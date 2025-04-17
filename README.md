## gohanMTG
What should we have for dinner today?

## cloneしたときにして欲しいこと
```
make tailwind
```
を実行して、tailwindをインストールしてください
node_modulesディレクトリが生成されば成功です。

## そのほか
ただコンテナに入るとrootユーザーとして入ることになってしまいます。
その状態でアプリケーション作ったりすると、ホストのファイル編集時に権限が足りなくてメンドイかもしれません。
```
make django
make mysql
```
のコマンドで、一般ユーザーとしてそれぞれのコンテナに入れるのでよければ使ってください。

