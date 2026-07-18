import { probeCapabilities } from "./probe.js";

const report = await probeCapabilities();
console.log(JSON.stringify(report, null, 2));
