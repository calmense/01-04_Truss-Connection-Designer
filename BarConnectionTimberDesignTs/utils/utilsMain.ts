import { getKmod } from './utilsMaterialProperties';
import { getDistances } from './utilsDistances';
import { characteristicValues, shearCapacity } from './utilsFastenerCapacity';
import { checkNoSheets, calcAxialMemberCheck, blockFailureCheckAxial } from './utilsChecks';
import { ConnectionDesignerInput, ConnectionDesignerOutput } from './utilsTypes';
import { calcPossibleFastener } from  './utilsPossibleFastener';

export function connectionDesigner(connectionDesignerInput: ConnectionDesignerInput): ConnectionDesignerOutput {
    // Extract input properties from connectionDesignerInput
    let { serviceClass, loadDurationClass, beam, timberGrade, width, height, axialForce, fastenerGrade, fastenerDiameter, sheetGrade, sheetThickness, sheetNo } = connectionDesignerInput;

    // 0 - General
    const thickness: number = width / 2;
    
    // 1 - Function to get modification factor
    const [kMod, gamma, chi] = getKmod(serviceClass, loadDurationClass);

    // 2 - Function to get modification factor
    const [minDistancesListTimber, minDistancesListSteel, distancesListRequired] = getDistances(fastenerDiameter);

    // 3 - calc fastener properties
    const [f_ub, M_yrk, f_h0k, f_halphak] = characteristicValues(fastenerDiameter, timberGrade, fastenerGrade, 0);

    // 4 - calc fastener caacity
    const [F_vrd, F_vrd1, F_vrd2, F_vrk1, F_vrk2, F_vrkf, F_vrkg, F_vrkh, F_vrkl, F_vrkm] = shearCapacity(fastenerDiameter, thickness, timberGrade, fastenerGrade, 0, chi);

    // 5 - calc possible fastener
    const [noTotal, noTotalEffective, noAxial, noAxialEffective,noPerp, F_vrdTotal, fastenerCheck, distances] = calcPossibleFastener(height, fastenerDiameter, axialForce, distancesListRequired, F_vrd, sheetNo);

    // 6 - number of sheets
    sheetNo = checkNoSheets(noAxial, sheetNo);

    // 7 - recalculate fastener capacity
    const [F_vrdNew, F_vrd1New, F_vrd2New, F_vrk1New, F_vrk2New, F_vrkfNew, F_vrkgNew, F_vrkhNew, F_vrklNew, F_vrkmNew] = shearCapacity(fastenerDiameter, thickness, timberGrade, fastenerGrade, 0, chi);

    // 8 - recalc possible fastener
    const [noTotalNew, noTotalEffectiveNew, noAxialNew, noAxialEffectiveNew,noPerpNew, F_vrdTotalNew, fastenerCheckNew, distancesFinal] = calcPossibleFastener(height, fastenerDiameter, axialForce, distancesListRequired, F_vrdNew, sheetNo);

    // 9 - axial member check
    const [A_net, f_ct0k, f_ctd, force, sigma_ct0d, befct, etaAxialCheck] = calcAxialMemberCheck(width, height, noPerpNew, fastenerDiameter, axialForce, timberGrade, sheetNo, chi, sheetThickness);
    
    // 10 - block faiure 
    const [Lh, Lv, Ant, Anv, VeffRd, etaBlockFailure] = blockFailureCheckAxial(fastenerGrade, noPerpNew, noAxialNew, fastenerDiameter, sheetThickness, distancesFinal, axialForce, sheetNo);

    // Define the output object
    const connectionDesignerOutput: ConnectionDesignerOutput = {
        kMod: kMod,
        gamma: gamma,
        chi: chi,
        minDistancesListTimber: minDistancesListTimber,
        minDistancesListSteel: minDistancesListSteel,
        distancesListRequired: distancesListRequired,
        fub: f_ub,
        Myrk: M_yrk,
        fh0k: f_h0k,
        fhalphak: f_halphak,
        Fvrd: F_vrd,
        Fvrd_1: F_vrd1,
        Fvrd_2: F_vrd2,
        Fvrk_1: F_vrk1,
        Fvrk_2: F_vrk2,
        Fvrk_f: F_vrkf,
        Fvrk_g: F_vrkg,
        Fvrk_h: F_vrkh,
        Fvrk_l: F_vrkl,
        Fvrk_m: F_vrkm,
        sheetNo: sheetNo,
        noTotal: noTotal,
        noTotalEffective: noTotalEffective,
        noAxial: noAxial,
        noAxialEffective: noAxialEffective,
        noPerp: noPerp,
        FvrdTotal: F_vrdTotal,
        fastenerCheck: fastenerCheck,
        distancesFinal: distancesFinal,
        Anet: A_net,
        fct0k: f_ct0k,
        fctd: f_ctd,
        force: force,
        sigmact0d: sigma_ct0d,
        befct: befct,
        etaAxialCheck: etaAxialCheck,
        Lh: Lh,
        Lv: Lv,
        Ant: Ant,
        Anv: Anv,
        VeffRd: VeffRd,
        etaBlockFailure: etaBlockFailure
    };

    return connectionDesignerOutput;
}