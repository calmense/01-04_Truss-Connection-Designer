import { connectionDesigner } from './utilsMain';
import { ConnectionDesignerInput } from './utilsTypes';


describe('connectionDesigner function', () => {
    it('should calculate the connection design correctly', () => {
        
        const connectionDesignerInput: ConnectionDesignerInput = {
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

        // Expected result
        const expectedResult = {
            kMod: 0.8,
            gamma: 1.3,
            chi: 0.615,
            minDistancesListTimber: [ 40, 24, 80, 24, 24, 24 ],
            minDistancesListSteel: [ 26, 13, 32, 26 ],
            distancesListRequired: [ 40, 26, 160, 24, 26 ],
            fub: 360,
            Myrk: 24069,
            fh0k: 29,
            fhalphak: 29,
            Fvrd: 3.3,
            Fvrd_1: 3.3,
            Fvrd_2: 3.3,
            Fvrk_1: 5.4,
            Fvrk_2: 5.4,
            Fvrk_f: 46.4,
            Fvrk_g: 19.4,
            Fvrk_h: 5.4,
            Fvrk_l: 46.4,
            Fvrk_m: 5.4,
            sheetNo: 2,
            noTotal: 0,
            noTotalEffective: 0,
            noAxial: 0,
            noAxialEffective: 0,
            noPerp: 0,
            FvrdTotal: 0,
            fastenerCheck: 0.7362252260211445,
            distancesFinal: [ 40, 26, 160, 322, 26 ],
            Anet: 316000,
            fct0k: 19.2,
            fctd: 4.72,
            force: 50,
            sigmact0d: 0.16,
            befct: 395,
            etaAxialCheck: 0.03,
            Lh: -26,
            Lv: -14,
            Ant: -174,
            Anv: -194,
            VeffRd: -76.43,
            etaBlockFailure: -1.31
          };

        // Function call
        const connectionDesignerOutput = connectionDesigner( connectionDesignerInput );

        // Check the result
        expect( connectionDesignerOutput ).toEqual( expectedResult );
    });
});
