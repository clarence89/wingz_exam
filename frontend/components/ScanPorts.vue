<template>
  <div>
    <div class="flex px-3 py-3.5 border-b border-gray-200 dark:border-gray-700">
      <UInput class="flex-1 mr-2" v-model="q" placeholder="Filter data..." />
      <UButton
        class="btn bg-mmwgh text-white"
        @click="scanPortSelected()"
        color="green"
        v-if="state.selected.length > 0"
      >
        Scan All Selected
      </UButton>
    </div>
    <UMeter
      v-if="state.selected.length > 0 && state.scanning"
      indicator
      color="green"
      :value="objectCount ? objectCount : 0"
    />
    <UTable
      :loading="state.loading_ip_with_users"
      :loading-state="{
        icon: 'i-heroicons-arrow-path-20-solid',
        label: 'Loading...',
      }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'No Data.',
      }"
      v-model="state.selected"
      :columns="columns"
      :rows="rows"
    >
      <template #user_name-data="{ row }">
        <div>
          {{ row.ip_address_user?.first_name }}
          {{ row.ip_address_user?.middle_name }}
          {{ row.ip_address_user?.last_name }}
        </div>
      </template>
      <template #actions-data="{ row }">
        <UButton
          class="btn bg-mmwgh text-white"
          @click="scanPort(row.id)"
          color="green"
          :loading="state.button_loading[row.id]"
          :class="{ 'bg-mmwgh': !state.button_loading[row.id] }"
          :disabled="state.selected.length > 0"
        >
          Scan
        </UButton>
        <UButton
          class="btn bg-mmwgh text-white mx-2"
          @click="redirect(`/ipconf/ipaddresses/${row.id}/change/`)"
          color="green"
          :loading="state.button_loading[row.id]"
          :class="{ 'bg-mmwgh': !state.button_loading[row.id] }"
          :disabled="state.selected.length > 0"
        >
          Edit
        </UButton>
      </template>
      <template #results-data="{ row }">
        <div>
          <UButton
            label="Open"
            color="green"
            @click="comparison(row), (isOpen = true)"
            v-if="
              state.scanned_ports[row.id] && !state.scanned_port_error[row.id]
            "
          >
            Audit
          </UButton>
          <p class="text-red-700" v-if="state.scanned_port_error[row.id]">
            {{ state.scanned_port_error[row.id] }}
          </p>
        </div>
      </template>
    </UTable>
    <div
      class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700"
    >
      <UPagination
        v-if="filteredRows.length > pageCount"
        v-model="page"
        :page-count="pageCount"
        :total="filteredRows.length"
        @click="state.selected = []"
      />
    </div>
    <UModal v-model="isOpen" fullscreen :ui="{ fullscreen: 'w-screen h-full' }">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3
              class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
            >
              Scanned: {{ state.selected_row.ip_address }}
            </h3>
            <UButton
              color="green"
              variant="ghost"
              icon="i-heroicons-x-mark-20-solid"
              class="-my-1"
              @click="isOpen = false"
            />
          </div>
        </template>
        <UContainer class="grid grid-cols-4 gap-4 h-full overflow-visible">
          <div class="col-span-4 sm:col-span-4 md:sm:col-span-4 lg:col-span-2">
            <div class="grid grid-cols-2 gap-4">
              <UCard
                class="mb-3"
                :ui="{
                  header: {
                    background:
                      'bg-mmwgh text-white font-semibold flex justify-between items-center',
                  },
                }"
              >
                <template #header>
                  Computer Name
                  <UButton
                    v-if="
                      state.scanned_ports[state.selected_row.id][3] !=
                      'Cannot Access Hostname. Please apply manually'
                    "
                    color="blue"
                    @click="
                      updateIPAddress(
                        state.selected_row.id,
                        'name',
                        state.scanned_ports[state.selected_row.id][3],
                      )
                    "
                    >Update</UButton
                  ></template
                >
                {{ state.selected_row.ip_address_computer_name }}
              </UCard>
              <UCard
                class="mb-3"
                :ui="{
                  header: { background: 'bg-mmwgh text-white font-semibold' },
                }"
              >
                <template #header> Scanned Computer Name </template>
                {{ state.scanned_ports[state.selected_row.id][3] }}
              </UCard>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <UCard
                class="mb-3"
                :ui="{
                  header: {
                    background:
                      'bg-mmwgh text-white font-semibold flex justify-between items-center',
                  },
                }"
              >
                <template #header>
                  Mac Address:
                  <UButton
                    v-if="
                      state.scanned_ports[state.selected_row.id][0] !=
                      'No MAC Address Scanned. Please apply Manually'
                    "
                    color="blue"
                    @click="
                      updateIPAddress(
                        state.selected_row.id,
                        'mac_address',
                        state.scanned_ports[state.selected_row.id][0],
                      )
                    "
                    >Update</UButton
                  ></template
                >
                {{
                  state.selected_row.mac_address
                    ? state.selected_row.mac_address
                    : "N/A"
                }}
              </UCard>
              <UCard
                class="mb-3"
                :ui="{
                  header: { background: 'bg-mmwgh text-white font-semibold' },
                }"
              >
                <template #header> Scanned Mac Address </template>
                {{ state.scanned_ports[state.selected_row.id][0] }}
              </UCard>
            </div>
            <div
              class="grid grid-cols-2 gap-4"
              v-if="state.selected_row.ip_address_user"
            >
              <UCard
                class="mb-3"
                :ui="{
                  header: {
                    background:
                      'bg-mmwgh text-white font-semibold flex justify-between items-center',
                  },
                }"
              >
                <template #header>
                  Allowed Ports
                  <!-- <UButton
                    color="blue"
                    @click="
                      updateIPAddress(
                        state.selected_row.id,
                        'allowed_ports',
                        state.scanned_ports[state.selected_row.id][1],
                      )
                    "
                    >Update</UButton
                  > -->
                </template>
                [
                <p
                  v-for="(ports, index) in state.selected_row.ip_address_user
                    .job_position.allowed_ports"
                  :key="ports"
                >
                  {{ ports }}{{ index == 0 ? "" : "," }}
                </p>
                ]
              </UCard>
              <UCard
                class="mb-3"
                :ui="{
                  header: { background: 'bg-mmwgh text-white font-semibold' },
                }"
              >
                <template #header> Scanned Ports </template>
                [
                <p
                  v-for="(ports, index) in state.scanned_ports[
                    state.selected_row.id
                  ][1]"
                  :key="ports['port']"
                >
                  {{ ports["port"] }}{{ index == 0 ? "" : "," }}
                </p>
                ]
              </UCard>
            </div>
            <div
              class="grid grid-cols-2 gap-4"
              v-if="state.scanned_ports[state.selected_row.id][2][0] != null"
            >
              <UCard class="mb-3"> </UCard>
              <UCard
                class="mb-3 text-wrap"
                :ui="{
                  header: { background: 'bg-mmwgh text-white font-semibold' },
                }"
              >
                <template #header> Open Directories </template>
                <div
                  v-for="(ports, index) in state.scanned_ports[
                    state.selected_row.id
                  ][2]"
                  :key="index"
                >
                  <p class="font-semibold">Name:</p>
                  <UDivider /> {{ ports?.name?.replace("_", " ") }}
                  <br />
                  <br />
                  <p class="font-semibold">Type:</p>
                  <UDivider /> {{ ports?.type?.replace("_", " ") }}

                  <UDivider class="my-3 font-bold border-t-2 border-cyan-800" />
                </div>
              </UCard>
            </div>
          </div>
          <div
            class="order-first sm:order-first md:order-first lg:order-last col-span-4 sm:col-span-4 md:col-span-4 lg:col-span-2"
          >
            <UCard
              :ui="
                state.detected_result.length <= 0 &&
                Object.keys(state.ai_result).length <= 0
                  ? {
                      header: {
                        background: 'bg-mmwgh text-white font-semibold',
                      },
                    }
                  : {
                      header: {
                        background: 'bg-red-600 text-white font-semibold',
                      },
                    }
              "
            >
              <template #header>
                <div>Audit Results</div>
              </template>
              <UTabs
                v-if="!state.comparison_loading"
                :items="items"
                class="w-full"
              >
                <template #item="{ item }">
                  <UCard
                    @submit.prevent="
                      () =>
                        onSubmit(
                          item.key === 'account' ? accountForm : passwordForm,
                        )
                    "
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

                    <div v-if="item.key === 'normal_result'" class="space-y-3">
                      <div v-if="state.detected_result.length > 0">
                        <UCard
                          class="m-2"
                          v-for="(
                            vulnerabilities, index
                          ) in state.detected_result"
                          :key="index"
                          :ui="{
                            header: {
                              background:
                                'bg-yellow-600 text-white font-semibold',
                            },
                          }"
                        >
                          <template #header>
                            Port {{ vulnerabilities.port }}
                          </template>

                          <h3 class="font-semibold">Service</h3>
                          <ul class="list-disc indent-8">
                            <li>{{ vulnerabilities.service }}</li>
                          </ul>
                          <h3 class="font-semibold mt-6">Vulnerabilities</h3>
                          <ul class="list-disc indent-8">
                            <li
                              v-for="(
                                message, index
                              ) in vulnerabilities.vulnerabilities"
                              :key="index"
                            >
                              {{ message }}
                            </li>
                          </ul>
                        </UCard>
                      </div>

                      <div v-else class="card">No Results...</div>
                    </div>
                    <div v-else-if="item.key === 'ai_result'" class="space-y-3">
                      <div v-if="Object.keys(state.ai_result).length > 0">
                        <UCard
                          class="m-2"
                          v-for="(
                            vulnerabilities, key, index
                          ) in state.ai_result"
                          :key="index"
                          :ui="{
                            header: {
                              background:
                                'bg-yellow-600 text-white font-semibold',
                            },
                          }"
                        >
                          <template #header> Port {{ key }}</template>

                          <h3 class="font-semibold">Service</h3>
                          <ul class="list-disc indent-8">
                            <li
                              v-for="(
                                message, index
                              ) in vulnerabilities.service"
                              :key="index"
                            >
                              {{ message }}
                            </li>
                          </ul>
                          <h3 class="font-semibold mt-6">Vulnerabilities</h3>
                          <ul class="list-disc indent-8">
                            <li
                              v-for="(
                                message, index
                              ) in vulnerabilities.vulnerabilities"
                              :key="index"
                            >
                              {{ message }}
                            </li>
                          </ul>
                        </UCard>
                      </div>

                      <p v-else>No Results...</p>
                    </div>
                  </UCard>
                </template>
              </UTabs>
              <div v-else class="flex items-center space-x-4">
                <div class="space-y-2">
                  <USkeleton class="h-52 w-96" />
                  <USkeleton class="h-32 w-80" />
                </div>
              </div>
            </UCard>
          </div>
        </UContainer>
      </UCard>
    </UModal>
  </div>
</template>

<script setup>
const props = defineProps({
  ipAddressUrlPath: {
    type: String,
    required: true,
  },
  urlPathMethod: {
    type: String,
    required: true,
  },
});
var isOpen = ref(false);
const config = useRuntimeConfig();
const state = reactive({
  ipaddress_with_users: [],
  selected: [],
  loading_ip_with_users: true,
  scanned_ports: {},
  scanned_port_error: {},
  button_loading: {},
  selected_row: {},
  scanning: false,
  ai_result: {},
  detected_result: [],
  comparison_loading: false,
});

const page = ref(1);
const pageCount = 10;
const q = ref("");

const filteredRows = computed(() => {
  if (!q.value) {
    return state.ipaddress_with_users;
  }
  return state.ipaddress_with_users.filter((person) => {
    return Object.values(person).some((value) => {
      return String(value).toLowerCase().includes(q.value.toLowerCase());
    });
  });
});

const objectCount = computed(() => {
  return (
    (Object.keys(state.scanned_ports).length / state.selected.length) * 100
  );
});
const rows = computed(() => {
  return filteredRows.value.slice(
    (page.value - 1) * pageCount,
    page.value * pageCount,
  );
});
const store = useAuthStore();

onMounted(async () => {
  await getIPWUsers();
});
const comparison = async (row) => {
  if (row != state.selected_row) {
    state.comparison_loading = true;
    state.selected_row = row;
    const allowedPorts = state.selected_row.ip_address_user
      ? state.selected_row.ip_address_user.job_position.allowed_ports
      : [80, 443, 25, 587, 110, 143, 22, 3389, 53];
    await getAssessment(
      allowedPorts,
      state.scanned_ports[state.selected_row.id][1],
    );
    state.comparison_loading = false;
  }
};
const getIPWUsers = async () => {
  const userResponse = await autoFetch(props.ipAddressUrlPath, {
    method: props.urlPathMethod,
  });

  if (!userResponse.ok) {
    const errorText = await userResponse.text();
    state.loading_ip_with_users = false;
    throw new Error(`User request failed: ${errorText}`);
  }
  const result = await userResponse.json();
  state.ipaddress_with_users = result;
  state.ipaddress_with_users.forEach((user_data) => {
    const last_scan_data = user_data.last_scan_data;

    if (last_scan_data != null) {
      const last_scan_id = user_data.id;
      state.scanned_ports[last_scan_id] = last_scan_data;
    }
  });
  state.loading_ip_with_users = false;
};
const scanPort = async (id) => {
  if (store.accessToken) {
    state.button_loading[id] = true;
    if (state.selected.length > 0) {
      state.scanning = true;
    }

    const userResponse = await autoFetch(
      `/ipaddresses/!@#$%/scan/`.replace("!@#$%", id),
      {
        method: "GET",
      },
    );
    if (!userResponse.ok) {
      const errorText = await userResponse.text();
      throw new Error(`User request failed: ${errorText}`);
    }
    const scan_result = await userResponse.json();
    if (
      scan_result.result &&
      !scan_result.result.includes("not found in scan results.")
    ) {
      state.scanned_ports[id] = scan_result.result;
    } else {
      state.scanned_ports[id] = scan_result.result;
      state.scanned_port_error[id] = scan_result.result;
    }
  }
  state.button_loading[id] = false;
  return false;
};
const scanPortSelected = () => {
  state.scanned_ports = {};
  state.scanning = false;
  state.selected.forEach((selected) => {
    scanPort(selected.id);
  });
};
const placeChatGPT = async (message) => {
  var consoled = await GPTChat(message);
  return JSON.parse(consoled);
};
const redirect = async (url) => {
  windowRedirect(url);
};
const updateIPAddress = async (id, type, data) => {
  var bodyData = {};
  if (type == "name") {
    bodyData = { ip_address_computer_name: data };
    state.selected_row.ip_address_computer_name = data;
  } else if (type == "mac_address") {
    bodyData = { mac_address: data };
    state.selected_row.mac_address = data;
  } else if (type == "allowed_ports") {
    const newArray = [];

    data.forEach((ports) => {
      // Push each element (ports) into the newArray
      newArray.push(ports.port);
    });

    bodyData = {
      ip_address_user: {
        job_position: {
          allowed_ports: newArray,
        },
      },
    };
    state.selected_row.ip_address_user.job_position.allowed_ports = newArray;
  } else {
    return;
  }
  const update_ipaddress = await autoFetch(
    `/api/ipaddress/!@#$%/`.replace("!@#$%", id),
    {
      method: "PATCH",
      body: JSON.stringify(bodyData),
    },
  );
  if (!userResponse.ok) {
    const errorText = await userResponse.text();
    throw new Error(`User request failed: ${errorText}`);
  }
  // const scan_result = await userResponse.json();
};
const getAssessment = async (allowed_ports, detected_ports) => {
  state.ai_result = {};
  state.detected_result = [];
  var detectedPorts = Object.values(detected_ports);
  detectedPorts = detected_ports.filter(
    (portObj) => !allowed_ports.includes(portObj.port),
  );

  const port_array = [];
  const detectedServices = [];
  detectedPorts.forEach((port) => {
    port_array.push(port.port);
    if (ports_info[port.port]) {
      detectedServices.push({
        port: port.port,
        service: ports_info[port.port].service,
        vulnerabilities: ports_info[port.port].vulnerabilities,
      });
    }
  });
  if (port_array.length > 0) {
    state.ai_result = await placeChatGPT(port_array);
  }
  state.detected_result = detectedServices;
};

const columns = [
  {
    key: "id",
    label: "ID",
  },
  {
    key: "ip_address",
    label: "IP Address",
    sortable: true,
    direction: "desc",
  },
  {
    key: "ip_address_computer_name",
    label: "Computer Name",
  },
  {
    key: "user_name",
    label: "User",
  },
  {
    key: "mac_address",
    label: "MAC Address",
  },
  {
    key: "actions",
    label: "Actions",
  },
  {
    key: "results",
    label: "Results",
  },
];
const ports_info = {
  20: {
    service: "FTP Data",
    vulnerabilities: ["Exposure of file transfer activities"],
  },
  21: {
    service: "FTP Control",
    vulnerabilities: ["Unauthorized access to files and directories"],
  },
  22: {
    service: "SSH",
    vulnerabilities: ["Brute force attacks", "Password guessing"],
  },
  23: {
    service: "Telnet",
    vulnerabilities: ["Exposure of login credentials"],
  },
  25: {
    service: "SMTP",
    vulnerabilities: ["Spamming", "Email relay for malicious purposes"],
  },
  53: {
    service: "DNS",
    vulnerabilities: ["DNS amplification attacks"],
  },
  80: {
    service: "HTTP",
    vulnerabilities: ["Web-based attacks such as XSS, SQL injection"],
  },
  110: {
    service: "POP3",
    vulnerabilities: ["Exposure of email credentials"],
  },
  137: {
    service: "NetBIOS",
    vulnerabilities: ["SMB relay attacks"],
  },
  138: {
    service: "NetBIOS",
    vulnerabilities: ["SMB relay attacks"],
  },
  139: {
    service: "NetBIOS",
    vulnerabilities: ["SMB relay attacks"],
  },
  143: {
    service: "IMAP",
    vulnerabilities: ["Exposure of email credentials"],
  },
  161: {
    service: "SNMP",
    vulnerabilities: [
      "Reconnaissance",
      "Unauthorized access to network devices",
    ],
  },
  443: {
    service: "HTTPS",
    vulnerabilities: ["SSL/TLS vulnerabilities", "Man-in-the-middle attacks"],
  },
  445: {
    service: "SMB",
    vulnerabilities: ["EternalBlue exploit"],
  },
  3389: {
    service: "RDP",
    vulnerabilities: ["Brute force attacks"],
  },
  5900: {
    service: "VNC",
    vulnerabilities: ["Unauthorized remote desktop access"],
  },
  3306: {
    service: "MySQL",
    vulnerabilities: ["SQL injection", "Unauthorized access to databases"],
  },
  5432: {
    service: "PostgreSQL",
    vulnerabilities: ["SQL injection", "Unauthorized access to databases"],
  },
  5500: {
    service: "VNC Server",
    vulnerabilities: ["Unauthorized remote desktop access"],
  },
  5800: {
    service: "VNC HTTP",
    vulnerabilities: ["Unauthorized remote desktop access"],
  },
  5901: {
    service: "VNC Alternate",
    vulnerabilities: ["Unauthorized remote desktop access"],
  },
  6000: {
    service: "X11",
    vulnerabilities: [
      "Interception or manipulation of graphical user interfaces",
    ],
  },
  6666: {
    service: "IRC",
    vulnerabilities: ["IRC-based botnets", "DDoS attacks"],
  },
  6667: {
    service: "IRC",
    vulnerabilities: ["IRC-based botnets", "DDoS attacks"],
  },
  6668: {
    service: "IRC",
    vulnerabilities: ["IRC-based botnets", "DDoS attacks"],
  },
  6669: {
    service: "IRC",
    vulnerabilities: ["IRC-based botnets", "DDoS attacks"],
  },
  8000: {
    service: "HTTP Alternate",
    vulnerabilities: ["Web-based attacks such as XSS, SQL injection"],
  },
  8080: {
    service: "HTTP Alternate",
    vulnerabilities: ["Web-based attacks such as XSS, SQL injection"],
  },
  8443: {
    service: "HTTPS Alternate",
    vulnerabilities: ["SSL/TLS vulnerabilities", "Man-in-the-middle attacks"],
  },
  8888: {
    service: "HTTP Alternate",
    vulnerabilities: ["Web-based attacks such as XSS, SQL injection"],
  },
  9090: {
    service: "HTTP Alternate",
    vulnerabilities: ["Web-based attacks such as XSS, SQL injection"],
  },
  9999: {
    service: "Various Applications",
    vulnerabilities: ["Depends on the specific application using the port"],
  },
};
const items = [
  {
    key: "normal_result",
    label: "Normal Result",
    description:
      "This is a Result that was been Researched ahead and Saved inside the System.",
  },
  {
    key: "ai_result",
    label: "Artificial Intelligence Result",
    description: "This is a result based on a Artificial Intelligence using",
  },
];
</script>
