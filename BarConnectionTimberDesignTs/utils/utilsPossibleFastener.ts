import * as math from 'mathjs'; // Import math module for mathematical functions
import { roundToBase, effectiveNumber } from './utilsDistances';

export function calcPossibleFastener(height: number, fastenerDiameter: number, axialForce: number, distances: number[], F_vrd: number, sheetNo: number): [number, number, number, number, number, number, number, number[]] {
    let [a1, a2, a3, a4, e1] = distances;

    let fastenerCheck: number = 2;
    let additionalFastener: number = 0;
    let noTotal: number = 0;
    let noTotalEffective: number = 0;
    let noAxial: number = 0;
    let noAxialEffective: number = 0;
    let noPerp: number = 0;
    let F_vrdTotal: number = 0;
    
    while (fastenerCheck > 0.8) {
        additionalFastener += 1;

        const noTotalReq: number = roundToBase(Math.abs(axialForce) / (F_vrd * (sheetNo * 2)), 1) + additionalFastener;
        const noPerpPos: number = Math.floor((height - 2 * a4) / a2);

        const noPerp: number = noTotalReq < noPerpPos ? Math.max(3, noTotalReq) : noPerpPos;
        a4 = (height - a2 * (noPerp - 1)) / 2;

        const noAxial: number = Math.max(roundToBase(noTotalReq / noPerp, 1), 1);
        const noAxialEffective: number = effectiveNumber(noAxial, a1, fastenerDiameter);

        const noTotal: number = noPerp * noAxial;
        const noTotalEffective: number = noAxialEffective * noPerp;

        const F_vrdTotal: number = F_vrd * noTotalEffective * (sheetNo * 2);
        fastenerCheck = Math.abs(axialForce) / F_vrdTotal;
    }

    const sheetLength: number = e1 + a1 * noAxial + a3 * 2;

    return [noTotal, noTotalEffective, noAxial, noAxialEffective, noPerp, F_vrdTotal, fastenerCheck, [a1, a2, a3, a4, e1]];
}
