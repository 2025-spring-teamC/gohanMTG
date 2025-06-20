#!/bin/bash
set -e

SSH_DIR=/home/ec2-user/.ssh
PROJECT_DIR=/home/ec2-user/gohanMTG

# パラメータストアからSSHキー取得・設定
echo "Setting up SSH key..."
SSH_KEY=$(aws ssm get-parameter --name "/gohanmtg/git/SSH_KEY" --with-decryption --query Parameter.Value --output text)
mkdir -p "$SSH_DIR"
echo "$SSH_KEY" > "$SSH_DIR/id_rsa"
sudo chmod 600 "$SSH_DIR/id_rsa"
sudo chown ec2-user:ec2-user "$SSH_DIR/id_rsa"

# git clone
echo "git clone..."
echo "$1"
sudo -u ec2-user bash -c "ssh-keyscan github.com >> $SSH_DIR/known_hosts"
git -c core.sshCommand="ssh -i $SSH_DIR/id_rsa" \
  clone --branch "$1" git@github.com:2025-spring-teamC/gohanMTG.git /home/ec2-user/gohanMTG

# .env 作成
echo " Creating .env file......"
PARAMETERS=$(aws ssm get-parameters-by-path --path "/gohanmtg/env/" --with-decryption)
echo "$PARAMETERS" | jq -r '.Parameters[] | "\(.Name | split("/")[-1])=\(.Value)"' > /home/ec2-user/gohanMTG/.env

# ALLOWED_HOSTSにEC2のプライベートIPアドレス追加
echo "Setting up ALLOWED_HOSTS..."
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4 \
  -H "X-aws-ec2-metadata-token: $TOKEN")
echo "${PRIVATE_IP}"
sed -i "/^ALLOWED_HOSTS/s|$|,${PRIVATE_IP}|" "$PROJECT_DIR/.env"

# RDS DNS名を設定
echo "setting up MYSQL_HOST..."
RDS_HOST=$(aws cloudformation describe-stacks \
  | jq -r '.Stacks[].Outputs[] | select(.OutputKey == "RDSDNS") | .OutputValue')
echo "${RDS_HOST}"
echo "MYSQL_HOST=${RDS_HOST}" >> "$PROJECT_DIR/.env"

# 各EC2のAZを追加（ログ管理用）
echo "Fetching Availability Zones..."
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone \
  -H "X-aws-ec2-metadata-token: $TOKEN")
echo "AZ=${AZ}" >> "$PROJECT_DIR/.env"

# RDS用証明書取得
echo "Retrieving RDS certificate......"
mkdir -p "$PROJECT_DIR/django/certs"
curl -o "$PROJECT_DIR/django/certs/rds-combined-ca-bundle.pem" \
  https://truststore.pki.rds.amazonaws.com/ap-northeast-1/ap-northeast-1-bundle.pem

#mariaDB設定
cat << EOF > ~/.my.cnf
[client-mariadb]
ssl=true
ssl-verify-server-cert=true
[client]
ssl-ca="$PROJECT_DIR/django/certs/rds-combined-ca-bundle.pem"
EOF

# mysqlユーザー作成
echo " Creating MySQL User......"
MYSQL_ROOT_USER=masteruser
MYSQL_ROOT_PASSWORD=$(grep '^MYSQL_ROOT_PASSWORD' "$PROJECT_DIR/.env" | cut -d '=' -f2)
MYSQL_USER=$(curl -s http://169.254.169.254/latest/meta-data/instance-id \
  -H "X-aws-ec2-metadata-token: $TOKEN")
MYSQL_PASSWORD=$(grep '^MYSQL_PASSWORD' "$PROJECT_DIR/.env" | cut -d '=' -f2)
MYSQL_DATABASE=$(grep '^MYSQL_DATABASE' "$PROJECT_DIR/.env" | cut -d '=' -f2)
mariadb -h "${RDS_HOST}" -P 3306 -u "${MYSQL_ROOT_USER}" -p"${MYSQL_ROOT_PASSWORD}" \
  -e "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD'; \
  GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, REFERENCES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%'; \
  FLUSH PRIVILEGES;"

echo "MYSQL_USER=${MYSQL_USER}" >> "$PROJECT_DIR/.env"

echo "Complete"