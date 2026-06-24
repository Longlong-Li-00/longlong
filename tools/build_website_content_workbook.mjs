import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  throw new Error("Usage: node build_website_content_workbook.mjs <input.json> <output.xlsx>");
}

const payload = JSON.parse(await fs.readFile(inputPath, "utf8"));
const workbook = Workbook.create();
const previewDir = path.resolve("data", "website_content_previews");
await fs.mkdir(previewDir, { recursive: true });

const headerFill = "#173A5E";
const headerFont = "#FFFFFF";
const accentFill = "#E8F0F7";
const borderColor = "#C8D5E2";

function columnWidth(header) {
  if (["id", "item_id", "field", "type", "category", "level", "status", "patent_type", "presentation_type"].includes(header)) return 20;
  if (["year", "date", "order", "visible", "selected", "volume", "issue", "pages"].includes(header)) return 13;
  if (["period", "year_or_period", "application_date", "grant_or_publication_date"].includes(header)) return 18;
  if (header.includes("title") || header.includes("name_")) return 42;
  if (header === "authors" || header === "inventors") return 55;
  if (header === "bibtex") return 68;
  if (["link", "url", "image", "source_filename"].includes(header)) return 46;
  if (header.includes("description") || header.includes("background") || header.includes("methods") || header.includes("contribution") || header.includes("result")) return 60;
  if (header === "notes") return 52;
  if (header.startsWith("value_")) return 56;
  if (["journal", "conference", "organization", "applicant"].includes(header)) return 34;
  return 24;
}

function excelColumn(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    value -= 1;
    result = String.fromCharCode(65 + (value % 26)) + result;
    value = Math.floor(value / 26);
  }
  return result;
}

function asExcelValue(header, value) {
  if (value === null || value === undefined) return "";
  if (["year", "order"].includes(header) && value !== "") return Number(value);
  if (["visible", "selected"].includes(header)) return value ? "TRUE" : "FALSE";
  if (["date", "application_date", "grant_or_publication_date"].includes(header) && /^\d{4}-\d{2}-\d{2}$/.test(String(value))) {
    return new Date(`${value}T00:00:00`);
  }
  return value;
}

function addValidation(sheet, headers, rowCount) {
  const validations = {
    type: ["journal", "review", "manuscript", "other"],
    selected: ["TRUE", "FALSE"],
    patent_type: ["granted_invention", "published_invention_application", "utility_model", "other"],
    presentation_type: ["oral", "poster"],
    category: ["scholarship", "academic_honor", "competition", "other"],
    visible: ["TRUE", "FALSE"],
  };
  for (const [header, values] of Object.entries(validations)) {
    const index = headers.indexOf(header);
    if (index < 0 || rowCount < 1) continue;
    const column = excelColumn(index);
    sheet.getRange(`${column}2:${column}${rowCount + 1}`).dataValidation = {
      rule: { type: "list", values },
    };
  }
}

for (const [sheetIndex, [sheetName, headers]] of Object.entries(payload.headers).entries()) {
  const records = payload.sheets[sheetName] || [];
  const sheet = workbook.worksheets.add(sheetName);
  const rows = [
    headers,
    ...records.map((record) => headers.map((header) => asExcelValue(header, record[header]))),
  ];
  const lastColumn = excelColumn(headers.length - 1);
  const lastRow = rows.length;
  const usedRange = sheet.getRange(`A1:${lastColumn}${lastRow}`);
  for (const textHeader of ["id", "item_id", "patent_number", "application_number", "doi"]) {
    const index = headers.indexOf(textHeader);
    if (index >= 0) {
      const column = excelColumn(index);
      sheet.getRange(`${column}1:${column}${lastRow}`).format.numberFormat = "@";
    }
  }
  usedRange.values = rows;
  const applicationNumberIndex = headers.indexOf("application_number");
  if (applicationNumberIndex >= 0 && records.length > 0) {
    const column = excelColumn(applicationNumberIndex);
    sheet.getRange(`${column}2:${column}${lastRow}`).formulas = records.map((record) => {
      const value = String(record.application_number || "").replaceAll('"', '""');
      return [value ? `="${value}"` : ""];
    });
  }
  usedRange.format = {
    font: { name: "Aptos", size: 10, color: "#1F2937" },
    verticalAlignment: "top",
    wrapText: true,
  };
  sheet.getRange(`A1:${lastColumn}1`).format = {
    fill: headerFill,
    font: { name: "Aptos", size: 10, bold: true, color: headerFont },
    verticalAlignment: "center",
    horizontalAlignment: "left",
    wrapText: true,
    borders: { preset: "outside", style: "thin", color: headerFill },
  };
  sheet.getRange(`A1:${lastColumn}1`).format.rowHeight = 28;
  if (lastRow > 1) {
    const body = sheet.getRange(`A2:${lastColumn}${lastRow}`);
    body.format.borders = {
      insideHorizontal: { style: "thin", color: borderColor },
      bottom: { style: "thin", color: borderColor },
    };
    body.format.rowHeight = ["publications", "cv", "projects"].includes(sheetName) ? 64 : 42;
    const table = sheet.tables.add(`A1:${lastColumn}${lastRow}`, true, `${sheetName.replace(/[^A-Za-z0-9]/g, "")}Table`);
    table.style = sheetIndex % 2 === 0 ? "TableStyleMedium2" : "TableStyleMedium9";
    table.showFilterButton = true;
  }
  headers.forEach((header, index) => {
    const column = excelColumn(index);
    sheet.getRange(`${column}1:${column}${lastRow}`).format.columnWidth = columnWidth(header);
  });
  for (const dateHeader of ["date", "application_date", "grant_or_publication_date"]) {
    const index = headers.indexOf(dateHeader);
    if (index >= 0 && lastRow > 1) {
      const column = excelColumn(index);
      sheet.getRange(`${column}2:${column}${lastRow}`).format.numberFormat = "yyyy-mm-dd";
    }
  }
  const notesIndex = headers.indexOf("notes");
  if (notesIndex >= 0 && lastRow > 1) {
    const notesColumn = excelColumn(notesIndex);
    sheet.getRange(`${notesColumn}2:${notesColumn}${lastRow}`).format.fill = accentFill;
  }
  addValidation(sheet, headers, records.length);
  sheet.freezePanes.freezeRows(1);
  sheet.showGridLines = false;
}

const summary = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  maxChars: 3000,
});
console.log(summary.ndjson);

for (const sheetName of ["profile", "publications", "patents", "conferences", "projects"]) {
  const headers = payload.headers[sheetName];
  const records = payload.sheets[sheetName] || [];
  const previewColumn = excelColumn(Math.min(headers.length, 5) - 1);
  const previewRow = Math.min(records.length + 1, 4);
  const check = await workbook.inspect({
    kind: "table",
    range: `${sheetName}!A1:${previewColumn}${previewRow}`,
    include: "values,formulas",
    tableMaxRows: 4,
    tableMaxCols: 5,
    maxChars: 2500,
  });
  console.log(check.ndjson);
}

for (const sheetName of Object.keys(payload.headers)) {
  const headers = payload.headers[sheetName];
  const records = payload.sheets[sheetName] || [];
  const lastColumn = excelColumn(headers.length - 1);
  const lastRow = records.length + 1;
  const preview = await workbook.render({
    sheetName,
    range: `A1:${lastColumn}${lastRow}`,
    scale: 0.8,
    format: "png",
  });
  await fs.writeFile(
    path.join(previewDir, `${sheetName}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`Workbook saved: ${outputPath}`);
