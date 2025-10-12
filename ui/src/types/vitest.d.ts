declare module 'vitest' {
  export const describe: (
    name: string,
    fn: () => void | Promise<void>
  ) => void;
  export const it: (
    name: string,
    fn: () => void | Promise<void>
  ) => void;
  export const expect: (value: unknown) => {
    toBeGreaterThan: (expected: number) => void;
    toBe: (expected: unknown) => void;
    not: {
      toThrow: () => void;
    };
  } & Record<string, (...args: unknown[]) => void>;
}
