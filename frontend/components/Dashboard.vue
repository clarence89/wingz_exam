<template>
  <div>
    <UTabs :items="items" class="w-full">
      <template #item="{ item }">
        <UCard

        >
          <template #header>
            <p
              class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
            >
              {{ item.label }}
            </p>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ item.description }}
            </p>
          </template>

          <div v-if="item.key === 'scan_port'" class="space-y-3">
            <ScanPorts
              :ipAddressUrlPath="`/api/ipaddress/ipaddresses_with_users/`"
              :urlPathMethod="'GET'"
            />
          </div>
          <div v-else-if="item.key === 'online_ip_scan'" class="space-y-3">
            <ScanPorts
              :ipAddressUrlPath="`/ipaddresses/scan/all`"
              :urlPathMethod="'GET'"
            />
          </div>
          <div v-else-if="item.key === 'reports'" class="space-y-3">
            <ReportComponent />
          </div>
        </UCard>
      </template>
    </UTabs>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
import { reactive } from "vue";

const items = [
  {
    key: "scan_port",
    label: "Scan Port",
    description:
      "Scan Ports and to ensure the allowed ports for a specified computer.",
  },
  {
    key: "online_ip_scan",
    label: "Scan all Online IP's",
    description:
      "Scans all Online IPS using a Minor Scan Algorithm with Actions for more Aggressive Scan",
  },
  {
    key: "reports",
    label: "Reports",
  },
];

const store = useAuthStore();
const state = reactive({
  abra: "aa",
});
</script>
