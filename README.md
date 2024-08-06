# BRAD (Behavior Recognition Action Decision)
Renamed from Image Recognition Action Decision to Behavior Recognition Action Decision
  
・[--ENGLISH](#english-ver)
・[--日本語](#日本語-ver)

## ・ENGLISH ver
(Translated at DeepL)
# Development Progress
Currently developing an BRAD to perform the task of cutting down wood in Minecraft.
  
- Real-time object detection of trees in Minecraft using YOLO v5.
- . /BRAD/Codes/Minecraft/Tree/ScreenCapture.py to run
  
- Code being produced to create dataset for behavior recognition model.
- . /BRAD/Codes/Minecraft/Tree/CaptureScreenKeys.py
  
## The following is filled in as a memo since we are still in the design phase for BRAD.

### BRAD working procedure:
- ##### Recognize actions and convert current video data to text from training data and current video data.
- ##### Select training data similar to long-term objectives to determine short-term objectives.
- ##### Determine short-term objectives based on the selected training data. By processing this recursively, the action plan becomes more specific.
- ##### If the current situation changes, the action plan is modified accordingly. The recursive process also allows the broad action plan to be changed as needed.

BRAD determines whether the objective and current situation are similar by taking into account various factors, such as past memories and current status obtained by BRAD as well as these action plan texts.

By generating action plans in text format, character recognition such as OCR can be used in conjunction.

### In order to implement BRAD:.
- ##### Required libraries:.
    - ###### Image Recognition
    - ###### Action Recognition
    - ###### Character Recognition

    The above must be processed accurately and at high speed.
      
    Libraries that can combine all three are desirable.
      
    It is also necessary to obtain information such as the location of objects in the image.
      
    Also, it is necessary to support time-series correspondence in both cases.
- ##### Model learned to act according to the action plan in the text
    If it is possible to generate plans to the deepest dimension, there is no need for a “model learned to act according to the action plan in the text.” However, to reduce the amount of computation, a model that generates a certain amount of action plans and then acts according to them is necessary.
- ##### Measuring data similarity
- ##### Efficient accumulation and use of data collected so far

### Reasons for action plans in text format:.
- Easily handle text recognition.
- By processing text well, rules that humans have can be easily dropped.
- Easy to see how the AI plans and acts.
- Can be applied as an auxiliary tool for humans to tell them appropriate action plans for the future.

### Disadvantages of action planning in text format
- Likely to lose information for a variety of reasons, including low dimensionality of the action plan and accuracy of action recognition
- Data volume may increase due to pre-determination of future action plans.
-As for the above, it is possible to save processing and data volume by inferring the near future action plan to a deep dimension and only inferring the far future action plan roughly.

###### In the future, a new method will be adopted to replace the text format.

### Example of the BRAD concept
As an example, in Minecraft, logs are collected, crafted into wood, and placed on the ground. To perform the task of,

### Roughly

---
- Go near the tree
- Dig for logs
- Craft logs into wood
- Install the wood.
---
#### This is a rough plan of action
#### If you detail the above,

---
- Go near the tree
    - Look around.
    - If you find a tree, head for it
- Dig for logs
    - Focus on the log
    - Digging for logs
    - Pick up the logs that drop
- Craft the log into wood
    - Open inventory
    - Move the cursor over the log you picked up
    - Retrieve the log
    - Move cursor to craft table
    - Place log on craft table
    - Hover over the crafted wood
    - Hover over the crafted wood
    - Move cursor to item slot
    - Place the wood in the item slot
    - Close inventory
- Place the wood
    - Place the item on the ground
    - Place the wood.
---
It can be as detailed as this.
As the plan of action becomes more detailed, eventually keystrokes become the lowest dimension of the plan.
#### For example,

---
- Set up the wood.
    - Set your viewpoint on the ground.
        - Mouse down for 0.5 seconds (example if the ground is around the area where the mouse is down for 0.5 seconds)
        - Confirm that the block selection display appears.
    - Place the wood
        - Right click.
        - Confirm that the wood is placed.
---Right-click to confirm wood is placed.
### Problems at this point:
- Variability in behavior recognition for objects and events.
- Combining multiple AIs may result in poor learning.

---
### Notes
Even if things do not go according to the action plan, the action plan is variable depending on the situation, and can cope with any situation.
The actions are selected based on the learning data that is similar to the current action history.
Similarities are identified for each dimension.
After executing the selected action plan, the system learns based on the difference in movement from the data for learning. (Compare with action plans of higher dimensions)
If the result is contrary to the ideal action, the probability of that action being selected is reduced.
The AI that executes the action also learns based on the reproducibility of the action plan. (Compare with lower dimensional action plans) <- Not necessary if action recognition is perfect.
If the action recognition technology and data are sufficient, imitation learning is possible with action recognition alone.
It will be possible to convert the events that occurred to text data as data compression.
For the behavior recognition model, classify without specifying the number of labels.
If possible, we would like to use a model that can automatically assign labels using unsupervised learning.

---
# ・日本語 ver

# 開発の進捗
現在マインクラフトで木材を伐採するタスクを実行するためのBRADを開発中
  
- YOLO v5 を使用してマインクラフト内の木をリアルタイムで物体検出した。
- ./BRAD/Codes/Minecraft/Tree/ScreenCapture.py から実行可能
  
- 行動認識モデル用のデータセットを作成するコードを製作中
- ./BRAD/Codes/Minecraft/Tree/CaptureScreenKeys.py から実行可能
  
## BRADについてはまだ設計段階なので、下記はメモとして記入している。

### BRADの動作手順：
- ##### 学習用データと現在の映像データを行動認識してテキストに変換する。
- ##### 短期的な目的を決定するために、長期的な目的と類似した学習データを選択する。
- ##### 選択した学習データを元に、短期的な目的を決定する。これを再帰的に処理することで、行動計画が具体的になっていく。
- ##### 現在の状況が変化した場合は、それに応じて行動計画を変更する。再帰的な処理により、必要に応じて大まかな行動計画も変更できる。

BRADはこれらの行動計画テキストと同時に自身が取得した過去の記憶や現在のステータスなど、様々な要素を加味して目的と現在の状況が類似しているか判断する。

テキスト形式で行動計画を生成することで、OCR等の文字認識を併用することができる。

### BRADを実現するにあたって:
- ##### 必要なライブラリ:
    - ###### 画像認識
    - ###### 行動認識
    - ###### 文字認識

    上記を高精度かつ高速で処理する必要がある。
      
    三つを併用できるライブラリが望ましい。
      
    画像内のどの位置に物体があるか、なども取得する必要がある。
      
    また、両方において時系列に対応に対応する必要がある。
- ##### テキストの行動計画通りに行動するよう学習したモデル
    次元の最深部まで計画を生成することができれば "テキストの行動計画通りに行動するよう学習したモデル" は必要ないが、計算量を削減するためある程度の行動計画を生成したのちそれに沿って動作するモデルが必要。
- ##### データの類似度を測る
- ##### これまで収集したデータの効率的な蓄積、利用

### テキスト形式で行動計画を立てる理由:
- 文字認識を容易に扱える
- 文章をうまく加工することで人間が持っているルールを簡単に落とし込める
- AIがどのような計画を立てて、どのように行動するのかを簡単に見ることができる。
- 将来の適切な行動計画を教えてくれる人間の補助的なツールにも応用できる。

### テキスト形式で行動計画を立てるデメリット
- 行動計画の次元の低さ、行動認識の精度など、様々な理由により情報を喪失してしまう可能性が高い
- 今後の行動予定をあらかじめ決定しておくため、データ容量が大きくなる可能性がある。
-上記に関しては近い未来の行動計画は深い次元まで推論し、遠い未来の行動計画は大まかな推論にとどめる事で処理やデータ量を節約することができる。

###### 将来的にはテキスト形式に変わる新しい方式をとる。

### BRADの考え方についての例
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
- 物体、事象に対する行動認識の多様性
- 複数のAIを組み合わせることにより、学習がうまく進まなくなる可能性

---
### 以下はメモ
尚、行動計画通りに物事が進まなかった場合でも行動計画は状況によって可変するため、あらゆる状況にも対処することができる。
これらの行動をどう選択するかは、現在までの行動履歴と類似した学習用データでの行動を選択する。
次元ごとに類似点を見極める。
選択した行動計画を実行した後、学習用データとの動きの差分を元に学習する。(より高次元の行動計画と照らし合わせる)
理想の行動と反した結果になった場合、その行動が選択される確率を低くする。
行動を実行する側のAIも行動計画の再現度を元に学習する。(より低次元の行動計画と照らし合わせる) <-行動認識が完璧にできれば必要ない。
行動認識技術とデータが十分にあれば、行動認識のみで模倣学習が可能。
データの圧縮として起きた事象をテキストデータに変換することができるようになる。
行動認識モデルについて、ラベルの個数を指定せずに分類をする。
可能なら教師なし学習を使用して自動的にラベルを付与することができるモデルを使用したい。

動作認識のデータセット
動作の内容をそれぞれ細かくする。
目の前のブロックを掘る:
- ブロックに視点を合わせる:
    - ブロックの存在する座標に視点を移動する(ブロックを物体検出)
        - 視点を45°方向に動かす
            - 45°方向にカーソルを移動する
    - (視点が合っていることを確認する)
        - "視点をブロックに合わせる"を認識する
- 破壊する
    - 3秒間採掘をする
        - 3秒間左クリックをする
    - (ブロックが破壊されたことを確認する)
        - "ブロックを破壊する"を認識する

