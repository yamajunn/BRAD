# ARAD (Action Recognition Action Decision)

・[--ENGLISH](#english-ver)
・[--日本語](#日本語-ver)

## ・ENGLISH ver
(Translated at DeepL)
# Development Progress
Currently developing an ARAD to perform the task of cutting down wood in Minecraft.
  
- Real-time object detection of trees in Minecraft using YOLO v5.
- . /ARAD/Codes/Minecraft/Tree/ScreenCapture.py to run
  
- Code being produced to create dataset for motion recognition model.
- . /ARAD/Codes/Minecraft/Tree/CaptureScreenKeys.py
  
## The following is entered as a note about ARAD, as it is still in the design stage.

### ARAD working procedure:
- ##### Recognize motion and convert current video data to text from training data and current video data.
- ##### Select training data similar to long-term objectives to determine short-term objectives.
- ##### Determine the short-term objective based on the selected training data. By processing this recursively, the action plan becomes more specific.
- ##### If the current situation changes, the action plan is modified accordingly. The recursive process also allows the broad action plan to be changed as needed.

ARAD takes into account these action plan texts as well as various factors, such as past memories and current status that it has acquired, to determine whether the objective and current situation are similar.

By generating action plans in text format, character recognition such as OCR can be used in conjunction.

### In order to implement ARAD:.
- ##### Required libraries:.
    - ###### Image Recognition
    - ###### Motion Recognition
    - ###### Character Recognition

    The above must be processed accurately and at high speed.
      
    Libraries that can combine all three are desirable.
      
    It is also necessary to obtain information such as the position of objects in the image.
      
    In addition, it is necessary to support time-series correspondence in both.
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
- Likely to lose information for a variety of reasons, including low dimensionality of the action plan and accuracy of motion recognition
- Data volume may increase due to pre-determination of future action plans.
-As for the above, it is possible to save processing and data volume by inferring the near future action plan to a deep dimension and only inferring the far future action plan roughly.

###### In the future, a new method will be adopted to replace the text format.

### Example of the ARAD concept
As an example, in Minecraft, logs are collected, crafted into wood, and placed on the ground. To perform the task of,

### Roughly.

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
---

### Problems at the moment: 
- Variety of motion recognition for objects and events
- Combining multiple AIs may result in poor learning.

---
### Notes.
Even if things do not go according to the action plan, the action plan is variable depending on the situation, so it can cope with any situation.
The actions are selected based on the learning data that is similar to the current action history.
Similarities are identified for each dimension.
After executing the selected action plan, the system learns based on the difference in movement from the data for learning. (Compare with action plans of higher dimensions)
If the result is contrary to the ideal action, the probability of that action being selected is reduced.
The AI that executes the action also learns based on the reproducibility of the action plan. (Compare with the lower dimensional action plan) <- Not necessary if the behavior recognition is perfect.
If there is enough data and technology for behavior recognition, it is possible to learn by imitation using only behavior recognition.
It will be possible to convert events to text data as data compression.
For the behavior recognition model, classify without specifying the number of labels.
If possible, we would like to use a model that can automatically assign labels using unsupervised learning.

---
# ・日本語 ver

# 開発の進捗
現在マインクラフトで木材を伐採するタスクを実行するためのARADを開発中
  
- YOLO v5 を使用してマインクラフト内の木をリアルタイムで物体検出した。
- ./ARAD/Codes/Minecraft/Tree/ScreenCapture.py から実行可能
  
- 動作認識モデル用のデータセットを作成するコードを製作中
- ./ARAD/Codes/Minecraft/Tree/CaptureScreenKeys.py から実行可能
  
## ARADについてはまだ設計段階なので、下記はメモとして記入している。

### ARADの動作手順：
- ##### 学習用データと現在の映像データを動作認識してテキストに変換する。
- ##### 短期的な目的を決定するために、長期的な目的と類似した学習データを選択する。
- ##### 選択した学習データを元に、短期的な目的を決定する。これを再帰的に処理することで、行動計画が具体的になっていく。
- ##### 現在の状況が変化した場合は、それに応じて行動計画を変更する。再帰的な処理により、必要に応じて大まかな行動計画も変更できる。

ARADはこれらの行動計画テキストと同時に自身が取得した過去の記憶や現在のステータスなど、様々な要素を加味して目的と現在の状況が類似しているか判断する。

テキスト形式で行動計画を生成することで、OCR等の文字認識を併用することができる。

### ARADを実現するにあたって:
- ##### 必要なライブラリ:
    - ###### 画像認識
    - ###### 動作認識
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
- 行動計画の次元の低さ、動作認識の精度など、様々な理由により情報を喪失してしまう可能性が高い
- 今後の行動予定をあらかじめ決定しておくため、データ容量が大きくなる可能性がある。
-上記に関しては近い未来の行動計画は深い次元まで推論し、遠い未来の行動計画は大まかな推論にとどめる事で処理やデータ量を節約することができる。

###### 将来的にはテキスト形式に変わる新しい方式をとる。

### ARADの考え方についての例
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
- 物体、事象に対する動作認識の多様性
- 複数のAIを組み合わせることにより、学習がうまく進まなくなる可能性

---
### 以下はメモ
尚、行動計画通りに物事が進まなかった場合でも行動計画は状況によって可変するため、あらゆる状況にも対処することができる。
これらの行動をどう選択するかは、現在までの行動履歴と類似した学習用データでの行動を選択する。
次元ごとに類似点を見極める。
選択した行動計画を実行した後、学習用データとの動きの差分を元に学習する。(より高次元の行動計画と照らし合わせる)
理想の行動と反した結果になった場合、その行動が選択される確率を低くする。
行動を実行する側のAIも行動計画の再現度を元に学習する。(より低次元の行動計画と照らし合わせる) <-動作認識が完璧にできれば必要ない。
動作認識技術とデータが十分にあれば、動作認識のみで模倣学習が可能。
データの圧縮として起きた事象をテキストデータに変換することができるようになる。
動作認識モデルについて、ラベルの個数を指定せずに分類をする。
可能なら教師なし学習を使用して自動的にラベルを付与することができるモデルを使用したい。