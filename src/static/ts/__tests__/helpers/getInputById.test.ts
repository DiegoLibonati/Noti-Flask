import { getInputById } from "@/helpers/getInputById";

describe("getInputById", () => {
  afterEach(() => {
    document.body.innerHTML = "";
  });

  describe("when the input exists", () => {
    it("should return the input with the matching id", () => {
      document.body.innerHTML = `<input class="js-input" id="username" />`;
      const result = getInputById("username");
      expect(result).toBeInTheDocument();
      expect(result).toHaveAttribute("id", "username");
    });

    it("should return the correct input when multiple inputs are present", () => {
      document.body.innerHTML = `
        <input class="js-input" id="username" />
        <input class="js-input" id="password" />
        <input class="js-input" id="email" />
      `;
      const result = getInputById("password");
      expect(result).toHaveAttribute("id", "password");
    });

    it("should return the first matching input when ids are unique", () => {
      document.body.innerHTML = `<input class="js-input" id="email" type="email" />`;
      const result = getInputById("email");
      expect(result).toBeInstanceOf(HTMLInputElement);
    });
  });

  describe("when the input does not exist", () => {
    it("should return undefined when no inputs are in the DOM", () => {
      expect(getInputById("username")).toBeUndefined();
    });

    it("should return undefined when no input matches the id", () => {
      document.body.innerHTML = `<input class="js-input" id="username" />`;
      expect(getInputById("email")).toBeUndefined();
    });

    it("should return undefined when the element lacks the js-input class", () => {
      document.body.innerHTML = `<input id="username" />`;
      expect(getInputById("username")).toBeUndefined();
    });
  });
});
