import { defineStore } from "pinia";

export const usePriceStore = defineStore({
  id: "priceStore",
  state: () => ({
    // チケット価格情報一覧
    prices: [],
  }),
  getters: {
    // すべてのチケット価格情報
    allPrices: (state) => state.prices,
  },

  // actions: {
  // },
});
