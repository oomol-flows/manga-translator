import fs from "fs";

export default async function (params, context) {
  if (!fs.existsSync(params["sourceDir"])) {
    fs.mkdirSync(params["sourceDir"]);
  }
  if (!fs.existsSync(params["outputDir"])) {
    fs.mkdirSync(params["outputDir"]);
  }
  return { 
    sourceDir: params["sourceDir"],
    outputDir: params["outputDir"]
  };
}
