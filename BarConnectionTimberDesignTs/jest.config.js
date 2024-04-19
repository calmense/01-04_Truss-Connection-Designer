module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/utils'],
    transform: {
      '^.+\\.ts$': 'ts-jest',
    },
  };