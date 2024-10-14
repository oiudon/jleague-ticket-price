<template>
  <Line :data="chartData" :options="options" />
</template>

<script>
import { ref, watch } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "LineChart",
  components: {
    Line,
  },
  props: {
    dates: {
      type: Array,
      default: () => [], // ファクトリ関数で新しい配列を返す
    },
    prices: {
      type: Array,
      default: () => [], // ファクトリ関数で新しい配列を返す
    },
  },
  setup(props) {
    // グラフデータを作成
    const chartData = ref({
      labels: props.dates,
      datasets: [
        {
          label: "チケット価格",
          data: props.prices,
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    });

    // グラフの設定
    const options = ref({
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "日付", // X軸ラベル
          },
        },
        y: {
          beginAtZero: true, // Y軸を0からスタート
          title: {
            display: true,
            text: "価格 (円)", // Y軸ラベル
          },
        },
      },
    });

    // propsの変更を監視してグラフデータを更新
    watch(
      () => [props.dates, props.prices],
      () => {
        chartData.value = {
          labels: props.dates,
          datasets: [
            {
              label: "チケット価格",
              data: props.prices,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        };
      },
      { immediate: true } // 初回マウント時にも更新
    );

    return {
      chartData,
      options,
    };
  },
};
</script>
