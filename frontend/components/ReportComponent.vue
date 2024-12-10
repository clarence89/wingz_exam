<template>
  <div>
    <!-- Create user input here -->
    <!-- <input type="date" v-model="state.search_date" placeholder="Search Date" /> -->
    <div class="flex">
      <input
        class="flex-grow px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500"
        type="text"
        v-model="state.search"
        placeholder="Search"
      />
      <button
        class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg"
        @click="exportToExcel"
      >
        Export to Excel
      </button>
    </div>
    <UTable :columns="columns" :rows="state.search_data" />
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from "vue";
import ExcelJS from "exceljs";
import { saveAs } from "file-saver";

const state = reactive({
  search_date: new Date().toISOString().split("T")[0],
  search: null,
  search_data: [],
});

const fetchData = async () => {
  try {
    const response = await autoFetch(`/api/ipaddress/?${buildSearchQuery()}`, {
      method: "GET",
    });
    if (response.status !== 200) {
      throw new Error(`User request failed with status ${response.status}`);
    }
    const scanResult = await response.json();
    state.search_data = scanResult;
    return scanResult
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
};

onMounted(() => {
  fetchData();
});

function createDebounce() {
  let timeout = null;
  return function (fnc, delayMs) {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      fnc();
    }, delayMs || 5000);
  };
}

const debounceFetchData = createDebounce();

watch(
  () => [state.search_date, state.search],
  () => {
    debounceFetchData(fetchData, 2000);
  }
);

async function exportToExcel() {
  console.log()
  const scanResult = await fetchData();
  if (scanResult) {

    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet("Search Results");
    worksheet.addRow(["Search Results for: ", state.search ? state.search : 'ALL', "a total of", state.search_data.length]);

    worksheet.addRow(["Computer Name", "IP Address", "MAC Address"]);

    // Add data
    scanResult.forEach((item) => {
      worksheet.addRow([
        item.ip_address_computer_name,
        item.ip_address,
        item.mac_address,
      ]);
    });

    // Generate Excel file
    const buffer = await workbook.xlsx.writeBuffer();

    // Save Excel file
    saveAs(new Blob([buffer]), "search_results.xlsx");
  }
}

function buildSearchQuery() {
  let query = [];
  // if (state.search_date) query.push(`created_at=${state.search_date}`);
  if (state.search) query.push(`q=${state.search}`);
  return query.join("&");
}
const columns = [
  {
    key: "ip_address_computer_name",
    label: "Computer Name",
    sortable: true,
  },
  {
    key: "ip_address",
    label: "IP Address",
  },
  {
    key: "mac_address",
    label: "MAC Address",
  },
];
</script>
