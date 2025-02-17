export default {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/tests/jest.setup.js"],
  transform: {
    "^.+\\.js?$": "babel-jest"
  },
};
