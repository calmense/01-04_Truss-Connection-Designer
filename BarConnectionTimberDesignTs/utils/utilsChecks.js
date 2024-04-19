"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.calcAxialMemberCheck = exports.getEtaMax = exports.checkNoSheets = exports.blockFailureCheckAxial = exports.compressionMemberCheck = exports.tensionMemberCheck = void 0;
const utilsMaterialProperties_1 = require("./utilsMaterialProperties"); // Importing functions for material properties (assuming they are defined elsewhere)
// Function to check shear member utilization
function tensionMemberCheck(thickness, height, noPerpendicular, diameter, tensionForce, timberGrade, noSheet, chi, thicknessSheet) {
    // Get glulam properties
    const [grade, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05] = (0, utilsMaterialProperties_1.getTimberProperties)(timberGrade);
    // Calculate design shear resistance
    const k_t = 0.4;
    const f_td = Math.round(f_t0k * chi * k_t * 100) / 100;
    // Effective length factor
    const b_ef = thickness - thicknessSheet * 0.5 * Math.min(noSheet, 2);
    // Calculate net area
    const A_net = height * b_ef - noPerpendicular * diameter * b_ef;
    // Calculate force
    tensionForce = tensionForce / 2;
    // Calculate stress
    const sigma_t0d = Math.round((tensionForce) / A_net * 1000 * 100) / 100;
    // Calculate utilization ratio
    const eta = Math.round(sigma_t0d / f_td * 100) / 100;
    return [A_net, f_t0k, f_td, tensionForce, sigma_t0d, Math.round(b_ef * 100) / 100, eta];
}
exports.tensionMemberCheck = tensionMemberCheck;
// Function to check shear member utilization
function compressionMemberCheck(thickness, height, noPerpendicular, diameter, compressionForce, timberGrade, noSheet, chi, thicknessSheet) {
    // Get glulam properties
    const [grade, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05] = (0, utilsMaterialProperties_1.getTimberProperties)(timberGrade);
    // Calculate design shear resistance
    const f_cd = Math.round(f_c0k * chi * 100) / 100;
    // Effective length factor
    const k_t = 1;
    const b_ef = thickness - thicknessSheet * 0.5 * Math.min(noSheet, 2);
    // Calculate net area
    const A_net = height * b_ef;
    // Calculate force
    compressionForce = Math.abs(compressionForce / 2);
    // Calculate shear stress
    const sigma_c0d = Math.round(compressionForce / A_net * 1000 * 100) / 100;
    // Calculate utilization ratio
    const eta = Math.round(sigma_c0d / f_cd * 100) / 100;
    return [A_net, f_c0k, f_cd, compressionForce, sigma_c0d, Math.round(b_ef * 100) / 100, eta];
}
exports.compressionMemberCheck = compressionMemberCheck;
// Function to check shear block failure
function blockFailureCheckAxial(steelGrade, noPerp, noAxial, diameter, thickness, distancesFinal, axialForce, noSheet) {
    const d0 = diameter + 0.6;
    thickness = thickness;
    // Get tensile and yield strength of steel
    const [f_u, f_y] = (0, utilsMaterialProperties_1.getTensileStrength)(steelGrade);
    // Calculate lengths
    const a1 = distancesFinal[0];
    const a2 = distancesFinal[1];
    const e1 = distancesFinal[4];
    const Lh = a2 * (noPerp - 1);
    const Lv = a1 * (noAxial - 1) + e1;
    // Calculate effective areas
    const Ant = (Lh - (noPerp - 1) * d0) * thickness * noSheet;
    const Anv = 2 * (Lv - (noAxial - 0.5) * d0) * thickness * noSheet;
    // Calculate design shear resistance
    const V_eff1Rd = Math.round(((f_u * Ant) / 1.25 + (f_y * Anv) / (Math.sqrt(3) * 1)) / 1000 * 100) / 100;
    // Calculate utilization ratio
    const eta = Math.round(Math.abs(axialForce) / V_eff1Rd * 100) / 100;
    return [Lh, Lv, Ant, Anv, V_eff1Rd, eta];
}
exports.blockFailureCheckAxial = blockFailureCheckAxial;
// check no of sheets
function checkNoSheets(noAxial, sheetNo) {
    let test = 0;
    if (noAxial >= 4) {
        test = 1;
        if (test == 1) {
            sheetNo = 2;
        }
        else {
            const a = 2;
        }
    }
    return sheetNo;
}
exports.checkNoSheets = checkNoSheets;
// calculate max eta
function getEtaMax(ClassList) {
    const fastenerCheckList = [];
    const tensionMemberCheckList = [];
    const compressionMemberList = [];
    const axialBlockFailureList = [];
    for (const beam of ClassList) {
        // checks
        fastenerCheckList.push(beam.fastenerCheck);
        tensionMemberCheckList.push(beam.tensionMemberCheck);
        compressionMemberList.push(beam.compressionMemberCheck);
        axialBlockFailureList.push(beam.axialBlockFailureCheck);
    }
    const fastenerCheckMax = Math.max(...fastenerCheckList);
    const tensionMemberCheckMax = Math.max(...tensionMemberCheckList);
    const compressionMemberMax = Math.max(...compressionMemberList);
    const axialBlockFailureMax = Math.max(...axialBlockFailureList);
    const fastenerCheckMaxIndex = fastenerCheckList.indexOf(fastenerCheckMax);
    const tensionMemberCheckMaxIndex = tensionMemberCheckList.indexOf(tensionMemberCheckMax);
    const compressionMemberMaxIndex = compressionMemberList.indexOf(compressionMemberMax);
    const axialBlockFailureMaxIndex = axialBlockFailureList.indexOf(axialBlockFailureMax);
    return [fastenerCheckMax, tensionMemberCheckMax, compressionMemberMax, axialBlockFailureMax, fastenerCheckMaxIndex, tensionMemberCheckMaxIndex, compressionMemberMaxIndex, axialBlockFailureMaxIndex];
}
exports.getEtaMax = getEtaMax;
function calcAxialMemberCheck(width, height, noPerp, fastenerDiameter, axialForce, timberGrade, sheetNo, chi, sheetThickness) {
    let A_net, f_ct0k, f_ctd, Force, sigma_ct0d, befct, eta;
    if (axialForce > 0) {
        [A_net, f_ct0k, f_ctd, Force, sigma_ct0d, befct, eta] = tensionMemberCheck(width, height, noPerp, fastenerDiameter, axialForce, timberGrade, sheetNo, chi, sheetThickness);
    }
    else {
        [A_net, f_ct0k, f_ctd, Force, sigma_ct0d, befct, eta] = compressionMemberCheck(width, height, noPerp, fastenerDiameter, axialForce, timberGrade, sheetNo, chi, sheetThickness);
    }
    return [A_net, f_ct0k, f_ctd, Force, sigma_ct0d, befct, eta];
}
exports.calcAxialMemberCheck = calcAxialMemberCheck;
