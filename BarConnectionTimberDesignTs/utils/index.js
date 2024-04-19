"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const utilsMain_1 = require("./utilsMain");
const connectionDesignerInput = {
    serviceClass: 1,
    loadDurationClass: "permanent",
    beam: 1,
    timberGrade: "GL24h",
    width: 400,
    height: 800,
    axialForce: 100,
    fastenerGrade: "S235",
    fastenerDiameter: 8,
    sheetGrade: "S235",
    sheetThickness: 5,
    sheetNo: 2,
};
// Function call
const connectionDesignerOutput = (0, utilsMain_1.connectionDesigner)(connectionDesignerInput);
// TypeScript main.ts
console.log(connectionDesignerOutput);
