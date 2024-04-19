"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.calcPossibleFastener = exports.getDistances = exports.calcMaxDistances = exports.roundToBase = exports.calcMinDistancesSteel = exports.effectiveNumber = exports.calcMinDistancesTimber = void 0;
const math = __importStar(require("mathjs")); // Import math module for mathematical functions
// Note: In TypeScript, we don't have direct support for streamlit like in Python.
// You might need to find alternative ways to create web applications in TypeScript.
// Function to calculate minimum distances between bolts for timber
function calcMinDistancesTimber(diameter, alpha) {
    // Calculate minimum distances based on given formulae
    const a1 = (3 + 2 * Math.abs(math.cos(alpha))) * diameter;
    const a2 = 3 * diameter;
    const a3t = Math.max(7 * diameter, 80);
    const a3c = Math.max(diameter * Math.abs(math.sin(alpha)), 3 * diameter);
    const a4t = Math.max((2 + 2 * Math.sin(alpha)) * diameter, 3 * diameter);
    const a4c = 3 * diameter;
    // Round the calculated values and return as a list
    return [Math.round(a1), Math.round(a2), Math.round(a3t), Math.round(a3c), Math.round(a4t), Math.round(a4c)];
}
exports.calcMinDistancesTimber = calcMinDistancesTimber;
// Function to calculate effective number of bolts
function effectiveNumber(n_row, a_1, diameter) {
    // Calculate effective number based on given formula
    let n_ef = Math.pow(n_row, 0.9);
    n_ef = Math.min(n_row, Math.pow(n_row, 0.9) * (a_1 / (13 * diameter)) ** (1 / 4));
    return parseFloat(n_ef.toFixed(2));
}
exports.effectiveNumber = effectiveNumber;
// Function to calculate minimum distances between bolts for steel
function calcMinDistancesSteel(diameter) {
    diameter += 0.6;
    // Calculate minimum distances based on given formula
    const e_1 = 3 * diameter;
    const e_2 = 1.5 * diameter;
    const p_1 = 3.75 * diameter;
    const p_2 = 3 * diameter;
    // Round the calculated values and return as a list
    return [Math.round(e_1), Math.round(e_2), Math.round(p_1), Math.round(p_2)];
}
exports.calcMinDistancesSteel = calcMinDistancesSteel;
function roundToBase(x, base) {
    return base * Math.round(x / base);
}
exports.roundToBase = roundToBase;
function calcMaxDistances(minDistancesListTimber, minDistancesListSteel, base) {
    const a1 = roundToBase(Math.max(minDistancesListTimber[0], minDistancesListSteel[2]), base);
    const a2 = roundToBase(Math.max(minDistancesListTimber[1], minDistancesListSteel[3]), base);
    const a3t = roundToBase(minDistancesListTimber[2], base);
    const a3c = roundToBase(minDistancesListTimber[3], base);
    const a3 = Math.max(a3t, a3c) * 2;
    const a4t = roundToBase(Math.max(minDistancesListTimber[4], minDistancesListSteel[1]), base);
    const a4c = roundToBase(Math.max(minDistancesListTimber[5], minDistancesListSteel[1]), base);
    const a4 = Math.max(a4t, a4c);
    const e1 = roundToBase(minDistancesListSteel[0], base);
    const distancesListRequired = [a1, a2, a3, a4, e1];
    return distancesListRequired;
}
exports.calcMaxDistances = calcMaxDistances;
function getDistances(fastenerDiameter) {
    const minDistancesListTimber = calcMinDistancesTimber(fastenerDiameter, 0);
    const minDistancesListSteel = calcMinDistancesSteel(fastenerDiameter);
    const distancesListRequired = calcMaxDistances(minDistancesListTimber, minDistancesListSteel, 1);
    return [minDistancesListTimber, minDistancesListSteel, distancesListRequired];
}
exports.getDistances = getDistances;
function calcPossibleFastener(height, fastenerDiameter, axialForce, distances, F_vrd, sheetNo) {
    let [a1, a2, a3, a4, e1] = distances;
    let fastenerCheck = 2;
    let additionalFastener = 0;
    let noTotal = 0;
    let noTotalEffective = 0;
    let noAxial = 0;
    let noAxialEffective = 0;
    let noPerp = 0;
    let F_vrdTotal = 0;
    while (fastenerCheck > 0.8) {
        additionalFastener += 1;
        const noTotalReq = roundToBase(Math.abs(axialForce) / (F_vrd * (sheetNo * 2)), 1) + additionalFastener;
        const noPerpPos = Math.floor((height - 2 * a4) / a2);
        const noPerp = noTotalReq < noPerpPos ? Math.max(3, noTotalReq) : noPerpPos;
        a4 = (height - a2 * (noPerp - 1)) / 2;
        const noAxial = Math.max(roundToBase(noTotalReq / noPerp, 1), 1);
        const noAxialEffective = effectiveNumber(noAxial, a1, fastenerDiameter);
        const noTotal = noPerp * noAxial;
        const noTotalEffective = noAxialEffective * noPerp;
        const F_vrdTotal = F_vrd * noTotalEffective * (sheetNo * 2);
        fastenerCheck = Math.abs(axialForce) / F_vrdTotal;
    }
    const sheetLength = e1 + a1 * noAxial + a3 * 2;
    return [noTotal, noTotalEffective, noAxial, noAxialEffective, noPerp, F_vrdTotal, fastenerCheck, [a1, a2, a3, a4, e1]];
}
exports.calcPossibleFastener = calcPossibleFastener;
