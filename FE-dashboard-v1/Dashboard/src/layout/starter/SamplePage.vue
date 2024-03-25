<template>
  <div class="row">
    <!-- Historical Data Line Chart -->
    <div class="col-6">
      <card type="chart">
        <template slot="header">
          <div class="row">
            <!-- Title -->
            <div class="col-sm-12 text-center">
              <h3>
                Historical Quantity Sold <b style=color:gold>`{{
                  historicalDataLineChart.activeCategory
                }}`</b> Bed Types in <b style=color:gold>{{ historicalDataLineChart.activeYear }}</b>
              </h3>
            </div>

            <!-- Select Category -->
            <div class="col-sm">
              <base-input label="Select Category">
                <div class="btn-group btn-group-toggle" data-toggle="buttons">
                  <label
                    v-for="category in ChartCategories"
                    :key="category"
                    class="btn btn-sm btn-primary btn-simple"
                    :class="{
                      active:
                        historicalDataLineChart.activeCategory === category,
                    }"
                    @click="setHistoricalCategory(category)"
                  >
                    {{ category }}
                  </label>
                </div>
              </base-input>
            </div>

            <!-- Select Year -->
            <div class="col-sm">
              <base-input label="Select Year">
                <select
                  class="form-control"
                  v-model="historicalDataLineChart.activeYear"
                  @change="setHistoricalYear"
                >
                  <option
                    v-for="year in HistoricalLineChartYears"
                    :key="year"
                    :value="year"
                    class="dropdown-item"
                  >
                    {{ year }}
                  </option>
                </select>
              </base-input>
            </div>
          </div>
        </template>

        <!-- line chart -->
        <line-chart
          style="height: 100%"
          ref="historicalChart"
          chart-id="historical-line-chart"
          :chart-data="historicalDataLineChart.chartData"
          :extra-options="historicalDataLineChart.extraOptions"
          :gradient-colors="historicalDataLineChart.gradientColors"
          :gradient-stops="historicalDataLineChart.gradientStops"
        />
      </card>
    </div>

    <!-- Forecast Data Line Chart -->
    <div class="col-6">
      <card type="chart">
        <template slot="header">
          <div class="row">
            <!-- Title -->
            <div class="col-sm-12 text-center">
              <h3>
                Forecast Quantity Sold  <b style=color:gold>`{{
                  forecastDataLineChart.activeCategory
                }}`</b> Bed Types in <b style=color:gold>{{ forecastDataLineChart.activeYear }}</b>
              </h3>
            </div>

            <!-- Select Category -->
            <div class="col-sm">
              <base-input label="Select Category">
                <div class="btn-group btn-group-toggle" data-toggle="buttons">
                  <label
                    v-for="category in ChartCategories"
                    :key="category"
                    class="btn btn-sm btn-primary btn-simple"
                    :class="{
                      active: forecastDataLineChart.activeCategory === category,
                    }"
                    @click="setForecastCategory(category)"
                  >
                    {{ category }}
                  </label>
                </div>
              </base-input>
            </div>

            <!-- Select Year -->
            <div class="col-sm">
              <base-input label="Select Year">
                <select
                  class="form-control"
                  v-model="forecastDataLineChart.activeYear"
                  @change="setForecastYear"
                >
                  <option
                    v-for="year in ForecastLineChartYears"
                    :key="year"
                    :value="year"
                    class="dropdown-item"
                  >
                    {{ year }}
                  </option>
                </select>
              </base-input>
            </div>
          </div>
        </template>

        <!-- line chart -->
        <line-chart
          style="height: 100%"
          ref="forecastChart"
          chart-id="forecast-line-chart"
          :chart-data="forecastDataLineChart.chartData"
          :extra-options="forecastDataLineChart.extraOptions"
          :gradient-colors="forecastDataLineChart.gradientColors"
          :gradient-stops="forecastDataLineChart.gradientStops"
        />
      </card>
    </div>

    <!-- Stacked Bar Chart -->
    <div class="col-12">
      <div class="col-sm-12 text-center">
        <h3>Beds bought by Age Groups in Year</h3>
      </div>
      <div class="row">
        <div class="col-sm-6">
          <base-input label="Select Year">
            <select
              class="form-control"
              v-model="ageDistYear"
              @change="setAgeDistData(ageDistYear, ageDistGroup)"
            >
              <option value="2021">2021</option>
              <option value="2022">2022</option>
              <option value="2023">2023</option>
            </select>
          </base-input>
        </div>
        <div class="col-sm-6">
          <base-input label="Select Age Groups">
            <select
              multiple
              class="form-control"
              v-model="ageDistGroup"
              @change="setAgeDistData(ageDistYear, ageDistGroup)"
            >
              <option value="20-24">20-24</option>
              <option value="25-29">25-29</option>
              <option value="30-34">30-34</option>
              <option value="35-39">35-39</option>
              <option value="40-44">40-44</option>
              <option value="45-49">45-49</option>
              <option value="50-54">50-54</option>
              <option value="55-59">55-59</option>
              <option value="60-64">60-64</option>
              <option value="65-69">65-69</option>
            </select>
          </base-input>
        </div>
      </div>

      <div class="col-sm-12">
        <div class="chart-area">
          <bar-chart
            style="height: 100%"
            chart-id="blue-bar-chart"
            :chart-data="blueBarChart.chartData"
            :gradient-stops="blueBarChart.gradientStops"
            :extra-options="blueBarChart.extraOptions"
          >
          </bar-chart>
        </div>
      </div>
    </div>

    <!-- Recommender -->
    <div class="col-sm-12 text-center">
      <h3>Recommender</h3>
    </div>
    <!-- User Profile -->
    <div
      class="col-sm-4 p-3"
      :class="{ active: activeSection === 'profile' }"
      @click="setActive('profile')"
      :style="{
        boxShadow: activeSection === 'profile' ? profileBoxShadowColor : '',
      }"
    >
      <h4>User Profile</h4>
      <div>
        <base-input
          label="Select Gender"
          :class="{ 'has-success': isGenderValid }"
        >
          <select class="form-control" v-model="gender">
            <option value="m">Male</option>
            <option value="f">Female</option>
          </select>
        </base-input>
      </div>
      <div>
        <base-input
          type="number"
          label="Enter age"
          v-model="age"
          placeholder="Enter age"
          :class="{ 'has-success': isAgeValid }"
          @input="updateProfileBoxShadow"
        >
        </base-input>
      </div>
    </div>

    <!-- Items Bought -->
    <div
      class="col-sm-4 p-3"
      :class="{ active: activeSection === 'purchases' }"
      @click="setActive('purchases')"
      :style="{
        boxShadow: activeSection === 'purchases' ? purchaseBoxShadowColor : '',
      }"
    >
      <h4>Add User Past Purchases</h4>
      <div>
        <!-- Model Dropdown -->
        <base-input label="Model" :class="{ 'has-success': isModelValid }">
          <select class="form-control" v-model="model">
            <option v-for="model in bedModels" :key="model">
              {{ model }}
            </option>
          </select>
        </base-input>
      </div>
      <!-- Size Dropdown -->
      <div>
        <base-input label="Size" :class="{ 'has-success': isSizeValid }">
          <select
            class="form-control"
            @change="updatePurchaseBoxShadow"
            v-model="size"
          >
            <option v-for="size in bedSizes" :key="size">{{ size }}</option>
          </select>
        </base-input>
      </div>

      <div
        v-if="activeSection === 'purchases' && model != null && size != null"
      >
        <!-- Add Item Bought -->
        <base-button
          round
          size="sm"
          type="success"
          @click="addToPurchaseHistory(model, size)"
          >Add <i class="tim-icons icon-simple-add"></i
        ></base-button>
      </div>
    </div>

    <!-- Display Items Bought -->
    <div
      class="col-sm-4 p-3"
      :class="{ active: activeSection === 'history' }"
      @click="setActive('history')"
      :style="{
        boxShadow: activeSection === 'history' ? historyBoxShadowColor : '',
      }"
    >
      <h4>User Purchase History</h4>
      <ul class="list-group list-group-flush">
        <li
          v-for="(item, index) in items_bought"
          :key="index"
          style="list-style-position: inside"
          @click="removeItem(item)"
        >
          {{ item.model }} {{ item.size }}
          <i class="tim-icons icon-simple-remove" style="color: red; cursor: pointer;"></i>
        </li>
      </ul>
    </div>

    <div class="col-sm-12 text-center">
      <div class="p-3" v-if="items_bought.length > 0">
        <base-button size="lg" type="success" @click="getRecommendations"
          >Get Recommendations <i class="tim-icons icon-zoom-split"></i
        ></base-button>
      </div>
      <hr />
      <!-- Beds Recommendation -->
      <div class="row" v-if="recommendations.length > 0">
        <div class="col-sm-12">
          <h4>
            Beds Recommendation based on similar user profiles and past
            purchases with similarity of
            <b style="color: #ba54f5">{{ similarityPercentage }}%</b>
          </h4>
        </div>
        <card
          class="col-sm-4"
          style="width: 20rem"
          v-for="recommendation in recommendations"
          :key="recommendation"
        >
          <img
            slot="image"
            class="card-img-top"
            :src="recommendation.image_url"
            alt="Card image cap"
          />
          <div class="card-text" style="color: #ba54f5">
            <h4>Model: {{ recommendation.model }}</h4>
            <h4>Size: {{ recommendation.size }}</h4>
            <h4>Price: SGD {{ recommendation.price }}</h4>
            <h4>
              Profit Maximising Price: SGD
              {{ recommendation.profit_maximising_price.toFixed(2) }}
            </h4>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";
import * as chartConfigs from "@/components/Charts/config";
import config from "@/config";
import axios from "axios";

export default {
  name: "starter-page",
  components: {
    LineChart,
    BarChart,
  },
  data() {
    return {
      ageDistYear: 2021,
      ageDistGroup: [],
      items_bought: [],
      age: null,
      gender: null,
      size: null,
      model: null,
      similarityPercentage: null,
      recommendations: [],
      profileBoxShadowColor: "", // Initialize box shadow color
      purchaseBoxShadowColor: "", // Initialize box shadow color
      historyBoxShadowColor: "", // Initialize box shadow color
      isProfileLoading: true,
      activeSection: "",
      bedModels: [], // diff bed models
      bedSizes: ["single", "super single", "queen", "king"],
      borderColorMap: {
        Single: config.colors.primary,
        "Super Single": config.colors.info,
        Queen: config.colors.teal,
        King: config.colors.danger,
      },
      selectedYear: 2021,
      historicalData: [],
      forecastData: [],
      ageDistributionData: [],
      historicalDataLineChart: {
        activeCategory: "Single",
        activeYear: 2021,
        chartData: {
          datasets: [{}],
          labels: [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
          ],
        },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0],
      },
      forecastDataLineChart: {
        activeCategory: "Single",
        activeYear: 2024,
        chartData: {
          datasets: [{}],
          labels: [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
          ],
        },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.2, 0],
      },
      blueBarChart: {
        chartData: {
          datasets: [{}],
          labels: [
            "20-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65+",
          ],
        },
        extraOptions: chartConfigs.barChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
      },
    };
  },
  mounted() {
    // historical and forecast end points
    axios
      .post("http://localhost:8081/generate_forecast")
      .then((response) => {
        // historical Data
        const historicalData = response.data.historical_data;
        this.historicalData = this.convertData(historicalData);
        this.getHistoricalData(2021, "All");

        // forecast Data
        const forecastData = response.data.forecast_data;
        this.forecastData = this.convertData(forecastData);
        this.getForecastData(2024, "All");
      })
      .catch((error) => {
        console.error("Error fetching forecast:", error);
      });

    // bar chart age group end points
    axios
      .post("http://localhost:5001/age_distribution", {
        year: 2021,
        age_groups: [],
      })
      .then((response) => {
        // Age Group Distribution Data
        const ageDistributionData = response.data;
        this.ageDistributionData = ageDistributionData;
        this.convertDataToDatasets(this.ageDistributionData);
      })
      .catch((error) => {
        console.error("Error fetching forecast:", error);
      });

    // get models
    axios
      .get("http://localhost:5002/models")
      .then((response) => {
        this.bedModels = response.data.models;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  computed: {
    ChartCategories() {
      return ["Single", "Super Single", "Queen", "King", "All"];
    },
    HistoricalLineChartYears() {
      return this.historicalData.map((data) => data.year);
    },
    ForecastLineChartYears() {
      return this.forecastData.map((data) => data.year);
    },
    isAgeValid() {
      return !isNaN(this.age) && this.age > 0;
    },
    isGenderValid() {
      return this.gender !== null;
    },
    isModelValid() {
      return this.model !== null;
    },
    isSizeValid() {
      return this.size !== null;
    },
  },
  methods: {
    removeItem(item) {
      // Filter out the clicked item
      this.items_bought = this.items_bought.filter((i) => i !== item);
    },
    setAgeDistData(year = this.ageDistYear, age_groups = this.ageDistGroup) {
      axios
        .post("http://localhost:5001/age_distribution", {
          year: year,
          age_groups: age_groups,
        })
        .then((response) => {
          // Age Group Distribution Data
          const ageDistributionData = response.data;
          this.ageDistributionData = ageDistributionData;
          this.convertDataToDatasets(this.ageDistributionData);
        })
        .catch((error) => {
          console.error("Error fetching forecast:", error);
        });
    },

    addToPurchaseHistory(model, size) {
      const existingItem = this.items_bought.find(
        (item) => item.model === model && item.size === size
      );

      if (existingItem) {
        this.$notify(
          "Item already added! Bed Model:" + model + " Bed Size: " + size
        );
        return;
      }
      // Item does not exist, add it to the array
      this.items_bought.push({ model: model, size: size });
      this.updateHistoryBoxShadow();
    },
    getRecommendations() {
      const requestBody = {
        age: this.age,
        gender: this.gender,
        items_bought: this.items_bought,
      };
      axios
        .post("http://localhost:5002/recommend", requestBody)
        .then((response) => {
          this.similarityPercentage = (
            response.data.cosine_similarity * 100
          ).toFixed(2);
          this.recommendations = response.data.recommendation;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateProfileBoxShadow() {
      // Update box shadow color based on input validity
      this.profileBoxShadowColor =
        this.isGenderValid && this.isAgeValid
          ? "0 0 20px rgba(0, 255, 0, 0.7)"
          : "0 0 20px rgba(255, 0, 0, 0.7)";
    },
    updatePurchaseBoxShadow() {
      this.purchaseBoxShadowColor =
        this.size && this.model
          ? "0 0 20px rgba(0, 255, 0, 0.7)"
          : "0 0 20px rgba(255, 0, 0, 0.7)";
    },
    updateHistoryBoxShadow() {
      this.historyBoxShadowColor =
        this.items_bought.length > 0
          ? "0 0 20px rgba(0, 255, 0, 0.7)"
          : "0 0 20px rgba(255, 0, 0, 0.7)";
    },
    convertData(data) {
      const result = [];
      // Define borderColor for each bed type
      const borderColorMap = {
        Single: config.colors.primary,
        "Super Single": config.colors.info,
        Queen: config.colors.teal,
        King: config.colors.danger,
      };

      // Loop through each entry in the JSON data
      data.forEach((entry) => {
        const monthData = [];
        const year = parseInt(entry.Month.split("/")[2]);
        const existingYearIndex = result.findIndex(
          (item) => item.year === year
        );

        // Extract data for each bed type
        Object.keys(entry).forEach((key) => {
          if (key !== "Month") {
            const categoryLabel = key.replace("_", " ");
            monthData.push({ label: categoryLabel, data: entry[key] }); // Push an object with label and data
          }
        });

        // If the year already exists in the result, update its data
        if (existingYearIndex !== -1) {
          result[existingYearIndex].data.forEach((item, index) => {
            item.data.push(monthData[index].data);
          });
        } else {
          // If the year doesn't exist, add it to the result
          const yearObj = { year: year, data: [] };
          monthData.forEach((category, index) => {
            yearObj.data.push({
              label: category.label,
              data: [category.data],
              borderColor: borderColorMap[category.label], // Add borderColor based on the label
            });
          });
          result.push(yearObj);
        }
      });
      return result;
    },
    // Historical Line Chart Methods
    setHistoricalCategory(category) {
      this.$notify(
        "Currently Looking at historical data of <b style=color:gold>" +
          category +
          "</b> bed types in <b style=color:gold>" +
          this.historicalDataLineChart.activeYear +
          "</b>"
      );
      this.historicalDataLineChart.activeCategory = category;
      this.getHistoricalData(this.historicalDataLineChart.activeYear, category);
    },
    setHistoricalYear() {
      this.$notify(
        "Currently Looking at data of <b style=color:gold>" +
          this.historicalDataLineChart.activeCategory +
          "</b> bed types in <b style=color:gold>" +
          this.historicalDataLineChart.activeYear +
          "</b>"
      );

      this.getHistoricalData(
        this.historicalDataLineChart.activeYear,
        this.historicalDataLineChart.activeCategory
      );
    },
    getHistoricalData(selectedYear = 2021, selectedCategory = "All") {
      const yearData = this.historicalData.find(
        (data) => data.year === selectedYear
      );
      if (yearData) {
        // Check if the selected category is "All"
        let datasets = [];
        if (selectedCategory === "All") {
          // If selected category is "All", include all categories in the datasets
          datasets = yearData.data.map((category) => ({
            label: category.label,
            data: category.data,
            borderColor: category.borderColor,
            fill: true,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: category.borderColor,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: category.borderColor,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
          }));
        } else {
          // If a specific category is selected, find and include only that category in the datasets
          const selectedCategoryData = yearData.data.find(
            (data) => data.label === selectedCategory
          );
          if (selectedCategoryData) {
            datasets.push({
              label: selectedCategoryData.label,
              data: selectedCategoryData.data,
              borderColor: selectedCategoryData.borderColor,
            });
          }
        }

        const chartData = {
          datasets: datasets,
          labels: [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
          ],
        };

        this.historicalDataLineChart.activeCategory = selectedCategory;
        this.historicalDataLineChart.activeYear = selectedYear;
        this.historicalDataLineChart.chartData = JSON.parse(
          JSON.stringify(chartData)
        ); // Deep copy
        this.historicalDataLineChart.gradientColors =
          config.colors.primaryGradient;
        this.historicalDataLineChart.gradientStops = [1, 0.2, 0];
        this.$refs.historicalChart.updateGradients(
          this.historicalDataLineChart.chartData
        );
      }
    },

    // Forecast Line Chart Methods
    setForecastCategory(category) {
      this.$notify(
        "Currently Looking at forecast data of <b style=color:gold>" +
          category +
          "</b> bed types in <b style=color:gold>" +
          this.forecastDataLineChart.activeYear +
          "</b>"
      );
      this.forecastDataLineChart.activeCategory = category;
      this.getForecastData(this.forecastDataLineChart.activeYear, category);
    },
    setForecastYear() {
      this.$notify(
        "Currently Looking at data of <b style=color:gold>" +
          this.forecastDataLineChart.activeCategory +
          "</b> bed types in <b style=color:gold>" +
          this.forecastDataLineChart.activeYear +
          "</b>"
      );
      this.getForecastData(
        this.forecastDataLineChart.activeYear,
        this.forecastDataLineChart.activeCategory
      );
    },
    getForecastData(selectedYear = 2024, selectedCategory = "All") {
      const yearData = this.forecastData.find(
        (data) => data.year === selectedYear
      );
      if (yearData) {
        // Check if the selected category is "All"
        let datasets = [];
        if (selectedCategory === "All") {
          // If selected category is "All", include all categories in the datasets
          datasets = yearData.data.map((category) => ({
            label: category.label,
            data: category.data,
            borderColor: category.borderColor,
            fill: true,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: category.borderColor,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: category.borderColor,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
          }));
        } else {
          // If a specific category is selected, find and include only that category in the datasets
          const selectedCategoryData = yearData.data.find(
            (data) => data.label === selectedCategory
          );
          if (selectedCategoryData) {
            datasets.push({
              label: selectedCategoryData.label,
              data: selectedCategoryData.data,
              borderColor: selectedCategoryData.borderColor,
            });
          }
        }

        const chartData = {
          datasets: datasets,
          labels: [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
          ],
        };

        this.forecastDataLineChart.activeCategory = selectedCategory;
        this.forecastDataLineChart.activeYear = selectedYear;
        this.forecastDataLineChart.chartData = JSON.parse(
          JSON.stringify(chartData)
        ); // Deep copy
        this.forecastDataLineChart.gradientColors =
          config.colors.primaryGradient;
        this.forecastDataLineChart.gradientStops = [1, 0.2, 0];
        this.$refs.forecastChart.updateGradients(
          this.forecastDataLineChart.chartData
        );
      }
    },

    // Stacked Bar Chart Data
    convertDataToDatasets(data) {
      // Define datasets
      let datasets = [];
      const categories = Object.keys(data[0]).filter(
        (key) => key !== "Age_Group"
      );
      categories.forEach((category) => {
        datasets.push({
          label: category.replace("_", " "),
          fill: true,
          backgroundColor: this.borderColorMap[category.replace("_", " ")],
          borderColor: this.borderColorMap[category.replace("_", " ")],
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: data.map((item) => item[category]),
        });
      });

      // Set chartData
      const chartData = {
        datasets: datasets,
        labels:
          this.ageDistGroup.length == 0
            ? [
                "20-24",
                "25-29",
                "30-34",
                "35-39",
                "40-44",
                "45-49",
                "50-54",
                "55-59",
                "60-64",
                "65-69",
              ]
            : this.ageDistGroup.map((ageGroup) => ageGroup),
      };
      // Update chartData and related properties
      this.blueBarChart.chartData = JSON.parse(JSON.stringify(chartData)); // Deep copy
      this.blueBarChart.extraOptions = chartConfigs.barChartOptions;
      this.blueBarChart.gradientColors = config.colors.primaryGradient;
      this.blueBarChart.gradientStops = [1, 0.4, 0];
    },

    setActive(section) {
      this.activeSection = section;
    },
  },
};
</script>

<style>
.active {
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.7); /* Soft shadow effect */
  border-radius: 10px; /* Rounded corners */
  transition: box-shadow 0.3s ease; /* Smooth transition for box-shadow */
}
</style>
