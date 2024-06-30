# IRAD (Image Recognition Action Decision)

<!-- IRADは学習用データと現在の映像データを画像認識して得られたテキストを何らかの形式で保持し、長期的な目的が一致したテキストデータをもとに将来の大まかな短期的な目的を決定する。

上記で決定した短期的な目的と現在の状況が類似している学習データを元に将来の行動計画を決定する。
これは再帰的に処理することで次元が小さくなり、行動計画が具体的になっていく。

現在の状況が変化した場合はそれに伴って次元内の行動計画を変更する。
これも再帰的に処理することで、必要な場合は大まかな行動計画も変更することができる。

これらの行動計画テキストと同時にその時点での自身またはそれに関するステータスを保持しておく。
目的と現在の状況が類似しているか、ステータスも含めて判断する。

IRADは、学習用データと現在の映像データを画像認識して得られたテキストを保持し、長期的な目的が一致したテキストデータをもとに将来の大まかな短期的な目的を決定します。 -->
・[--ENGLISH](#english-ver)
・[--日本語](#日本語-ver)

## ・ENGLISH ver
(Translated at DeepL)
# Development Progress
Currently developing an IRAD to perform the task of cutting down wood in Minecraft.
  
Real-time object detection of trees in Minecraft using YOLO v5.
  
. /IRAD/Codes/Minecraft/Tree/ScreenCapture.py to run

## The following is filled in as a note since we are still in the design phase regarding IRAD.

### IRAD operating procedure:
- ##### Recognize images from training data and current video data and convert to text.
- ##### Select training data similar to the long-term objective to determine the short-term objective.
- ##### Determine the short-term objective based on the selected training data. By processing this recursively, the action plan becomes more specific.
- ##### If the current situation changes, the action plan is modified accordingly. The recursive process also allows the broad action plan to be changed as needed.

IRAD takes into account these action plan texts as well as various factors, such as past memories and current status that it has acquired, to determine whether the objective and current situation are similar.

By generating action plans in text format, character recognition such as OCR can be used in conjunction.

### In order to implement IRAD:.
- ##### Required libraries:.
    - ###### Image Recognition
    - ###### Character Recognition

    The above must be processed with high accuracy and high speed.
      
    Libraries that can combine the two are desirable.
      
    It is also necessary to obtain information such as the position of objects in the image.
      
    Also, it is necessary to support time-series correspondence in both.
- ##### Model learned to act according to the action plan in the text
    If it is possible to generate plans to the deepest dimension, there is no need for a "model learned to act according to the action plan in the text." However, to reduce the amount of computation, a model that generates a certain amount of action plans and then acts according to them is necessary.
- ##### Measuring data similarity
- ##### Efficient accumulation and use of data collected so far

### Reasons for action plans in text format:.
- Easily handle text recognition.
- By processing text well, rules that humans have can be easily dropped.
- Can see how the AI plans and acts.
- Can be applied to human aids that tell us appropriate future action plans.

### Disadvantages of action planning in text format
- Likely to lose information for a variety of reasons, including low dimensionality of action plans, accuracy of image recognition, etc.
- Data volume may increase due to pre-determination of future action plans.
-As for the above, it is possible to save processing and data by making the near future action plans deeper in dimension and the far future action plans rougher.

###### In the future, a new method will replace the text format.

### Example on the IRAD concept.
As an example, in Minecraft, logs are collected, crafted into wood, and placed on the ground. To perform the task of,

### Roughly.

--- .
- Go near the tree
- Dig for logs
- Craft logs into wood
- Install the wood.
--- ......................
#### This is a rough plan of action
#### If you detail the above,

---.
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
---.
It can be as detailed as this.
As the plan of action becomes more detailed, eventually keystrokes become the lowest dimension of the plan.
#### For example,

---.
- Set up the wood.
    - Set your viewpoint on the ground.
        - Mouse down for 0.5 seconds (example if the ground is around the area where the mouse is down for 0.5 seconds)
        - Confirm that the block selection display appears.
    - Place the wood
        - Right click.
        - Confirm that the wood is placed.
---Right-click to confirm wood is placed.
### Problems at the moment: ### Versatility of image recognition for objects and events
- Variety of image recognition for objects and events
- Combining multiple AIs may result in poor learning.

--- --- --- ### Notes.
### Notes
Even if things do not go according to the action plan, the action plan is variable depending on the situation, so it can handle any situation.
  
The actions are selected based on the learning data that is similar to the current action history.
  
Similarities are identified for each dimension.
  
After executing the selected action plan, the system learns based on the difference in movement from the data for learning. (Compare with higher dimensional action plans)
  
The AI on the side that executes the action also learns based on the reproducibility of the action plan. (Match with a lower dimensional action plan) <- Not necessary if image recognition is perfect.
  
If the result is contrary to the ideal action, the probability of that action being selected is reduced.
  
If image recognition technology and data are sufficient, imitation learning is possible with image recognition alone.
  
Convert events that have occurred to text data as data compression.
  
  
Currently developing IRAD to perform the task of felling wood in Minecraft.

Translated with DeepL.com (free version)

# ・日本語 ver

# 開発の進捗
現在マインクラフトで木材を伐採するタスクを実行するためのIRADを開発中
  
YOLO v5 を使用してマインクラフト内の木をリアルタイムで物体検出した。
  
./IRAD/Codes/Minecraft/Tree/ScreenCapture.py から実行可能

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