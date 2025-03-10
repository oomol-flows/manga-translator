import fs from "fs";

export default async function (params, context) {
  if (!fs.existsSync(params["outputDir"])) {
    fs.mkdirSync(params["outputDir"]);
  }
  return { 
    outputDir: params["outputDir"]
  };
}
