# IRAD (Image Recognition Action Decision)

<!-- IRADは学習用データと現在の映像データを画像認識して得られたテキストを何らかの形式で保持し、長期的な目的が一致したテキストデータをもとに将来の大まかな短期的な目的を決定する。

上記で決定した短期的な目的と現在の状況が類似している学習データを元に将来の行動計画を決定する。
これは再帰的に処理することで次元が小さくなり、行動計画が具体的になっていく。

現在の状況が変化した場合はそれに伴って次元内の行動計画を変更する。
これも再帰的に処理することで、必要な場合は大まかな行動計画も変更することができる。

これらの行動計画テキストと同時にその時点での自身またはそれに関するステータスを保持しておく。
目的と現在の状況が類似しているか、ステータスも含めて判断する。

IRADは、学習用データと現在の映像データを画像認識して得られたテキストを保持し、長期的な目的が一致したテキストデータをもとに将来の大まかな短期的な目的を決定します。 -->

## IRADについてはまだ設計段階なので、下記はメモとして記入している。

### IRADの動作手順：
- ##### 学習用データと現在の映像データを画像認識してテキストに変換する。
- ##### 短期的な目的を決定するために、長期的な目的と類似した学習データを選択する。
- ##### 選択した学習データを元に、短期的な目的を決定する。これを再帰的に処理することで、行動計画が具体的になっていく。
- ##### 現在の状況が変化した場合は、それに応じて行動計画を変更する。再帰的な処理により、必要に応じて大まかな行動計画も変更できる。

IRADはこれらの行動計画テキストと同時に自身が取得した過去の記憶や現在のステータスなど、様々な要素を加味して目的と現在の状況が類似しているか判断する。

テキスト形式で行動計画を生成することで、OCR等の文字認識を併用することができる。

### IRADを実現するにあたって:
- ##### 必要なライブラリ:
    - ###### 画像認識
    - ###### 文字認識

    上記を高精度かつ高速で処理する必要がある。
      
    二つを併用できるライブラリが望ましい。
      
    画像内のどの位置に物体があるか、なども取得する必要がある。
      
    また、両方において時系列に対応に対応する必要がある。
- ##### テキストの行動計画通りに行動するよう学習したモデル
    次元の最深部まで計画を生成することができれば "テキストの行動計画通りに行動するよう学習したモデル" は必要ないが、計算量を削減するためある程度の行動計画を生成したのちそれに沿って動作するモデルが必要。
- ##### データの類似度を測る
- ##### これまで収集したデータの効率的な蓄積、利用

### テキスト形式で行動計画を立てる理由:
- 文字認識を容易に扱える
- 文章をうまく加工することで人間が持っているルールを簡単に落とし込める
- AIがどのような計画を立てて、どのように行動するのかを見ることができる。
- 将来の適切な行動計画を教えてくれる人間の補助的なものにも応用できる。

### テキスト形式で行動計画を立てるデメリット
- 行動計画の次元の低さ、画像認識の精度など、様々な理由により情報を喪失してしまう可能性が高い
- 今後の行動予定をあらかじめ決定しておくため、データ容量が大きくなる可能性がある。
-上記に関しては近い未来の行動計画は次元を深くし、遠い未来の行動計画は大まかなものにすれば処理やデータを節約することができる。

###### 将来的にはテキスト形式に変わる新しい方式をとる。

### IRADの考え方についての例
例としてマインクラフトで原木を採取し、木材にクラフトして地面に設置する。というタスクを実行するには、

### 大まかに

---
- 木の近くへ行く
- 原木を掘る
- 原木をクラフトして木材にする
- 木材を設置する
---
#### これが大まかな行動計画
#### 上記を細かくすると、

---
- 木の近くへ行く
    - 周りを見渡す
    - 木を発見したらそちらへ向かう
- 原木を掘る
    - 原木に視点を合わせる
    - 原木を掘る
    - ドロップした原木を拾う
- 原木をクラフトして木材にする
    - インベントリを開く
    - 拾った原木にカーソルを合わせる
    - 原木を取得する
    - クラフトテーブルにカーソルを合わせる
    - 原木をクラフトテーブルにおく
    - クラフトされた木材にカーソルを合わせる
    - 木材を取得する
    - アイテムスロットにカーソルを合わせる
    - 木材をアイテムスロットにおく
    - インベントリを閉じる
- 木材を設置する
    - 地面に視点を合わせる
    - 木材を置く
---
このように細かくすることができる。
行動計画をより細かくしていくと、最終的にはキー操作が計画の最低次元となる。
#### 例を出すと、

---
- 木材を設置する
    - 地面に視点を合わせる
        - マウスを下に0.5秒間下げる(マウスを0.5秒間下に下げた辺りに地面がある場合の例)
        - ブロック選択表示が出たことを確認する
    - 木材を置く
        - 右クリックをする。
        - 木材が置かれたことを確認する。
---
### 現時点での問題点:
- 物体、事象に対する画像認識の多様性
- 複数のAIを組み合わせることにより、学習がうまく進まなくなる可能性

---
### 以下はメモ
尚、行動計画通りに物事が進まなかった場合でも行動計画は状況によって可変するため、あらゆる状況にも対処することができる。
  
これらの行動をどう選択するかは、現在までの行動履歴と類似した学習用データでの行動を選択する。
  
次元ごとに類似点を見極める。
  
選択した行動計画を実行した後、学習用データとの動きの差分を元に学習する。(より高次元の行動計画と照らし合わせる)
  
行動を実行する側のAIも行動計画の再現度を元に学習する。(より低次元の行動計画と照らし合わせる) <-画像認識が完璧にできれば必要ない。
  
理想の行動と反した結果になった場合、その行動が選択される確率を低くする。
  
画像認識技術とデータが十分にあれば、画像認識のみで模倣学習が可能。
  
データの圧縮として起きた事象をテキストデータに変換。
  
  
現在マインクラフトで木材を伐採するタスクを実行するためのIRADを開発中