"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.shearCapacity = exports.characteristicValues = void 0;
const utilsMaterialProperties_1 = require("./utilsMaterialProperties");
function characteristicValues(diameter, timberGrade, strengthClass, angle) {
    // Get the tensile strength of the timber
    const [f_ub, f_y] = (0, utilsMaterialProperties_1.getTensileStrength)(strengthClass);
    // Calculate the characteristic moment capacity
    const M_yrk = 0.3 * f_ub * Math.pow(diameter, 2.6);
    // Get the density of the timber
    const [grade, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05] = (0, utilsMaterialProperties_1.getTimberProperties)(timberGrade);
    // Calculate the characteristic value of the compression strength
    const f_h0k = 0.082 * (1 - 0.01 * diameter) * rho_k;
    // Calculate the angle correction factor
    const k_90 = 1.35 + 0.015 * diameter;
    // Calculate the characteristic value of the compression strength at the given angle
    const f_halphak = f_h0k / (k_90 * Math.pow(Math.sin(angle), 2) + Math.pow(Math.cos(angle), 2));
    // Determine the compression strength based on the angle
    const f_hk = angle === 0 ? f_h0k : f_halphak;
    // Return the tensile strength, moment capacity, and compression strength
    return [f_ub, Math.round(M_yrk), Math.round(f_h0k * 10) / 10, Math.round(f_halphak * 10) / 10];
}
exports.characteristicValues = characteristicValues;
function shearCapacity(diameter, thickness, timberGrade, strengthClass, angle, chi) {
    // Get characteristic values
    const [f_ub, M_yrk, f_h0k, f_halphak] = characteristicValues(diameter, timberGrade, strengthClass, angle);
    // Calculate the shear capacity based on different failure modes
    // 1 sheet
    const F_vrkf = Math.round(f_h0k * thickness * diameter / 1000 * 10) / 10;
    const F_vrkg = Math.round(f_h0k * thickness * diameter * (Math.sqrt(2 + (4 * M_yrk) / (f_h0k * diameter * Math.pow(thickness, 2))) - 1) / 1000 * 10) / 10;
    const F_vrkh = Math.round(2.3 * Math.sqrt(M_yrk * f_h0k * diameter) / 1000 * 10) / 10;
    // 2 sheets
    const F_vrkl = Math.round(f_h0k * thickness * diameter / 1000 * 10) / 10;
    const F_vrkm = F_vrkh;
    // Select the minimum shear capacity from the calculated values
    const F_vrk1 = Math.min(F_vrkf, F_vrkg, F_vrkh);
    const F_vrk2 = Math.min(F_vrkf, F_vrkh, F_vrkl, F_vrkm);
    const F_vrd1 = Math.round(F_vrk1 * chi * 10) / 10;
    const F_vrd2 = Math.round(F_vrk2 * chi * 10) / 10;
    const F_vrd = Math.min(F_vrd1, F_vrd2);
    // Return the shear capacity in kilonewtons (kN)
    return [F_vrd, F_vrd1, F_vrd2, F_vrk1, F_vrk2, F_vrkf, F_vrkg, F_vrkh, F_vrkl, F_vrkm];
}
exports.shearCapacity = shearCapacity;
