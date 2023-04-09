export {};

declare global {
  namespace SchoolMeal {
    interface ProcessEnv {
      HMAC_KEY_NAME: string;
    }
  }
}
