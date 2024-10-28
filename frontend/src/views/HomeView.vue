<template>
  <!-- メインコンテンツ -->
  <v-main>
    <!-- プログレスバー -->
    <div v-if="loading" id="loading">
      <v-progress-circular
        :indeterminate="loading"
        color="primary"
      ></v-progress-circular>
    </div>

    <v-container max-width="800px">
      <!-- メッセージ表示欄 -->
      <GlobalMessage />

      <p>※対象はJ1ホーム試合のみです</p>
      <p>試合を選択してください</p>

      <!-- 試合年セレクトボックス -->
      <v-select
        :items="matchYears.slice().reverse()"
        label="年"
        class="ma-2"
        v-model="yearSelected"
        max-width="150px"
      ></v-select>

      <!-- チーム名コンボボックス -->
      <v-combobox
        :items="teams"
        label="チーム"
        class="ma-2"
        v-model="teamSelected"
        max-width="500px"
      ></v-combobox>

      <!-- 試合タイトルセレクトボックス -->
      <v-select
        :items="matchTitles.slice().reverse()"
        label="試合"
        class="ma-2"
        v-model="matchSelected"
      ></v-select>

      <p>試合会場：{{ stadiumName }}</p>
      <!-- 座席カテゴリセレクトボックス -->
      <v-select
        :items="seatCategories"
        label="座席カテゴリ"
        class="ma-2"
        v-model="seatSelected"
        max-width="500px"
      ></v-select>

      <LineChart :prices="prices" :dates="dates" />
    </v-container>
  </v-main>
</template>

<script>
import { ref, onMounted, watch } from "vue";
// import { usePriceStore } from "../stores/price.js";
import { useMessageStore } from "../stores/message.js";
import api from "../services/api.js";
import GlobalMessage from "../components/GlobalMessage.vue";
// import axios from "axios";
import LineChart from "../components/LineChart.vue";

export default {
  name: "HomeView",
  components: {
    GlobalMessage,
    LineChart,
  },
  setup() {
    // ストアオブジェクトを取得
    // const priceStore = usePriceStore();
    const messageStore = useMessageStore();

    // チケット価格一覧
    const prices = ref([]);
    // チケット価格の日付一覧
    const dates = ref([]);

    // 開催年セレクトボックスの選択肢
    const matchYears = ref([]);
    // チームコンボボックスの選択肢
    const teams = ref([]);
    // 試合タイトルセレクトボックスの選択肢
    const matchTitles = ref([]);
    // 座席カテゴリセレクトボックスの選択肢
    const seatCategories = ref([]);
    // 試合情報一覧
    const matchTitleDatetime = ref([]);

    // 選択中の開催年
    const yearSelected = ref(null);
    // 選択中のチーム
    const teamSelected = ref(null);
    // 選択中の試合タイトル
    const matchSelected = ref(null);
    // 選択中の座席カテゴリ
    const seatSelected = ref(null);

    // スタジアム名
    const stadiumName = ref(null);

    // プログレスバーフラグ
    const loading = ref(true);

    // yearSelected の変更を監視し、変更があれば onYearSelectChange を呼び出す
    watch(yearSelected, () => {
      onYearSelectChange();
    });

    // teamSelected の変更を監視し、変更があれば onTeamSelectChange を呼び出す
    watch(teamSelected, () => {
      onTeamSelectChange();
    });

    // matchSelected の変更を監視し、変更があれば onMatchSelectChange を呼び出す
    watch(matchSelected, () => {
      onMatchSelectChange();
    });

    // seatSelected の変更を監視し、変更があれば onSeatSelectChange を呼び出す
    watch(seatSelected, () => {
      onSeatSelectChange();
    });


    // 開催年セレクトボックスの値が変更されたときに発動する関数
    const onYearSelectChange = () => {
      // プログレスバーを表示
      loading.value = true;
      // メッセージをクリア
      messageStore.clear();
      // 選択中のチーム一覧、試合タイトル、試合会場、座席カテゴリ、グラフをクリア
      teamSelected.value = null;
      matchSelected.value = null;
      stadiumName.value = null;
      seatSelected.value = null;
      seatCategories.value = [];
      prices.value = [];
      dates.value = [];

      api({
        // 開催年が選択されたらその年の試合があったチーム一覧を取得
        method: "get",
        url: `/teams/?year=${yearSelected.value}`,
      })
        .then((response) => {
          // 選択された年の試合タイトルと試合時間を取得
          teams.value = response.data.map((item) => item.team_name);
          // プログレスバーを非表示
          loading.value = false;
        })
        .catch((error) => {
          // エラー発生時はエラーメッセージを表示
          messageStore.setError(error);
          // プログレスバーを非表示
          loading.value = false;
        });
    };

    // チームコンボボックスの値が変更されたときに発動する関数
    const onTeamSelectChange = () => {
      // プログレスバーを表示
      loading.value = true;
      // メッセージをクリア
      messageStore.clear();
      // 選択中の試合タイトル、試合会場、座席カテゴリ、グラフをクリア
      matchSelected.value = null;
      stadiumName.value = null;
      seatSelected.value = null;
      seatCategories.value = [];
      prices.value = [];
      dates.value = [];

      api({
        // 開催年が選択されたらその年の試合一覧を取得
        method: "get",
        url: `/match-title-datetime/?year=${yearSelected.value}&team_name=${teamSelected.value}`,
      })
        .then((response) => {
          // 選択された年の試合タイトルと試合時間を取得
          matchTitleDatetime.value = response.data;

          // 曜日の配列
          const weekdays = ["日", "月", "火", "水", "木", "金", "土"];
          // セレクトボックスに表示する選択肢を作成
          matchTitles.value = response.data.map((item) => {
            // ISO 8601形式の日時文字列を解析
            const matchDateStr = item.match_datetime;

            // 正規表現を使って日時を抽出
            const [datePart, timePart] = matchDateStr.split('T');
            const [year, month, day] = datePart.split('-');
            const [hours, minutes] = timePart.split(':');

            // 1桁の月と日をそのまま使用（先頭に0を付けない）
            const monthStr = parseInt(month, 10); // 数字として月を取得
            const dayStr = parseInt(day, 10); // 数字として日を取得
            const weekdayStr =
              weekdays[new Date(`${year}-${month}-${day}`).getDay()]; // 曜日を取得

            // 形式に合わせて文字列を作成
            return `${monthStr}月${dayStr}日(${weekdayStr})${hours}:${minutes}　${item.match_title}　${item.competition_name}`;
          });
          // プログレスバーを非表示
          loading.value = false;
        })
        .catch((error) => {
          // エラー発生時はエラーメッセージを表示
          messageStore.setError(error);
          // プログレスバーを非表示
          loading.value = false;
        });
    };


    // 試合タイトルセレクトボックスの値が変更されたときに発動する関数
    const onMatchSelectChange = () => {
      // プログレスバーを表示
      loading.value = true;
      // メッセージをクリア
      messageStore.clear();
      // 選択中の試合タイトル、試合会場、座席カテゴリ、グラフをクリア
      stadiumName.value = null;
      seatSelected.value = null;
      prices.value = [];
      dates.value = [];
      if (matchSelected.value) {
        // 選択された試合タイトルの要素番号を取得
        const selectedIndex = matchTitles.value.indexOf(matchSelected.value);
        // 選択された試合タイトルの要素番号に該当する試合情報一覧を取得
        const selectedMatchInfo = matchTitleDatetime.value[selectedIndex];
        // 試合情報一覧からスタジアム名を取得
        stadiumName.value = selectedMatchInfo.stadium_name;
        // 試合情報一覧から試合タイトルを取得
        const matchTitle = selectedMatchInfo.match_title;
        // 試合日時の不要な部分を除外
        const matchDatetime = selectedMatchInfo.match_datetime.replace(
          /(:\d{2}):\d{2}.*$/,
          "$1"
        );

        api({
          // 試合タイトルが選択されたらその試合のスタジアムの座席カテゴリを取得
          method: "get",
          url: `/seat-categories/?team_name=ＦＣ町田ゼルビア&match_datetime=${matchDatetime}&match_title=${matchTitle}`,
        })
          .then((response) => {
            // 座席カテゴリを配列で取得
            seatCategories.value = response.data.map(
              (item) => item.seat_category_name
            );
            // プログレスバーを非表示
            loading.value = false;
          })
          .catch((error) => {
            // エラー発生時はエラーメッセージを表示
            messageStore.setError(error);
            // プログレスバーを非表示
            loading.value = false;
          });
      }
    };

    // 座席カテゴリセレクトボックスの値が変更されたときに発動する関数
    const onSeatSelectChange = () => {
      // プログレスバーを表示
      loading.value = true;
      // メッセージをクリア
      messageStore.clear();
      if (seatSelected.value) {
        // 選択された試合タイトルの要素番号を取得
        const selectedIndex = matchTitles.value.indexOf(matchSelected.value);
        // 選択された試合タイトルの要素番号に該当する試合情報一覧を取得
        const selectedMatchInfo = matchTitleDatetime.value[selectedIndex];
        // 試合情報一覧からスタジアム名を取得
        stadiumName.value = selectedMatchInfo.stadium_name;
        // 試合情報一覧から試合タイトルを取得
        const matchTitle = selectedMatchInfo.match_title;
        // 試合日時の不要な部分を除外
        const matchDatetime = selectedMatchInfo.match_datetime.replace(
          /(:\d{2}):\d{2}.*$/,
          "$1"
        );

        api({
          // 座席カテゴリが選択されたらその座席のチケット価格を取得
          method: "get",
          url: `/ticket-prices/?team_name=${teamSelected.value}&match_datetime=${matchDatetime}&match_title=${matchTitle}&seat_category_name=${seatSelected.value}`,
        })
          .then((response) => {
            // チケット価格を配列で取得
            prices.value = response.data.map((item) => item.price);
            // 登録日を配列で取得
            dates.value = response.data.map((item) => item.created_at);
            // プログレスバーを非表示
            loading.value = false;
          })
          .catch((error) => {
            // エラー発生時はエラーメッセージを表示
            messageStore.setError(error);
            // プログレスバーを非表示
            loading.value = false;
          });
      }
    };

    // コンポーネントがマウントされたときにAPIリクエストを送信
    onMounted(() => {
      api({
        // DBからチケット価格が登録されている試合の開催年を取得
        method: "get",
        url: "/ticket-years/",
      })
        .then((response) => {
          // DBに登録されている試合の開催年を配列で取得
          matchYears.value = response.data.map((item) => item.match_year);
          // セレクトボックスの初期値を設定
          yearSelected.value = Math.max(...matchYears.value);
        })
        .catch((error) => {
          // エラー発生時はエラーメッセージを表示
          messageStore.setError(error);
        });
    });

    return {
      prices,
      dates,
      matchYears,
      teams,
      matchTitles,
      seatCategories,
      yearSelected,
      teamSelected,
      matchSelected,
      onYearSelectChange,
      onMatchSelectChange,
      stadiumName,
      seatSelected,
      loading,
    };
  },
};
</script>

<style>
#loading {
  display: flex; /* Flexboxレイアウトを使用し、子要素を中央に揃える */
  justify-content: center; /* 子要素を横方向の中央に配置する */
  align-items: center; /* 子要素を縦方向の中央に配置する */
  width: 100%; /* 横幅を100%に設定し、画面全体に広がるようにする */
  height: 100vh; /* 高さをビューポートの高さ（100vh）に設定する */
  z-index: 9999; /* 他の要素の上に表示されるように z-index を最大値に近い数値に設定する */
  position: fixed; /* 固定位置に設定し、スクロールしても表示位置が変わらないようにする */
}
</style>
