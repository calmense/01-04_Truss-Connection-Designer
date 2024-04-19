"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.calcPossibleFastener = void 0;
const utilsDistances_1 = require("./utilsDistances");
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
        const noTotalReq = (0, utilsDistances_1.roundToBase)(Math.abs(axialForce) / (F_vrd * (sheetNo * 2)), 1) + additionalFastener;
        const noPerpPos = Math.floor((height - 2 * a4) / a2);
        const noPerp = noTotalReq < noPerpPos ? Math.max(3, noTotalReq) : noPerpPos;
        a4 = (height - a2 * (noPerp - 1)) / 2;
        const noAxial = Math.max((0, utilsDistances_1.roundToBase)(noTotalReq / noPerp, 1), 1);
        const noAxialEffective = (0, utilsDistances_1.effectiveNumber)(noAxial, a1, fastenerDiameter);
        const noTotal = noPerp * noAxial;
        const noTotalEffective = noAxialEffective * noPerp;
        const F_vrdTotal = F_vrd * noTotalEffective * (sheetNo * 2);
        fastenerCheck = Math.abs(axialForce) / F_vrdTotal;
    }
    const sheetLength = e1 + a1 * noAxial + a3 * 2;
    return [noTotal, noTotalEffective, noAxial, noAxialEffective, noPerp, F_vrdTotal, fastenerCheck, [a1, a2, a3, a4, e1]];
}
exports.calcPossibleFastener = calcPossibleFastener;
