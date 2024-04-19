import { connectionDesigner } from './utilsMain';
import { ConnectionDesignerInput } from './utilsTypes';


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

// Function call
const connectionDesignerOutput = connectionDesigner( connectionDesignerInput );

// TypeScript main.ts
console.log(connectionDesignerOutput);
