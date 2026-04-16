import http from "k6/http";
import { check, sleep } from "k6";

const baseUrl = __ENV.BASE_URL || "http://127.0.0.1:5000";

export const options = {
  scenarios: {
    products_crud_load: {
      executor: "ramping-vus",
      startVUs: 1,
      stages: [
        { duration: "20s", target: 5 },
        { duration: "40s", target: 15 },
        { duration: "20s", target: 0 }
      ],
      gracefulRampDown: "10s"
    }
  },
  thresholds: {
    http_req_failed: ["rate<0.02"],
    http_req_duration: ["p(95)<800"],
    checks: ["rate>0.98"]
  }
};

function createPayload() {
  const stamp = Date.now();
  return {
    name: `k6-product-${stamp}`,
    description: "load test product",
    price: 999000,
    in_stock: true
  };
}

export default function () {
  const headers = { "Content-Type": "application/json" };

  const createRes = http.post(
    `${baseUrl}/api/v1/products`,
    JSON.stringify(createPayload()),
    { headers }
  );

  const createOk = check(createRes, {
    "create status is 201": (r) => r.status === 201
  });

  if (!createOk) {
    sleep(1);
    return;
  }

  const created = createRes.json();
  const productId = created.id;

  check(http.get(`${baseUrl}/api/v1/products`), {
    "list status is 200": (r) => r.status === 200
  });

  check(http.get(`${baseUrl}/api/v1/products/${productId}`), {
    "get by id status is 200": (r) => r.status === 200
  });

  const updateRes = http.put(
    `${baseUrl}/api/v1/products/${productId}`,
    JSON.stringify({
      name: created.name + "-updated",
      description: "updated by k6",
      price: 1099000,
      in_stock: false
    }),
    { headers }
  );

  check(updateRes, {
    "update status is 200": (r) => r.status === 200
  });

  const deleteRes = http.del(`${baseUrl}/api/v1/products/${productId}`);
  check(deleteRes, {
    "delete status is 204": (r) => r.status === 204
  });

  sleep(1);
}
