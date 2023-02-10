
export type None = null | undefined

export type Optional<T> = T | None

export function some<T>(value: Optional<T>): value is T {
  return (value !== null && value !== undefined)
}

export function none<T>(value: Optional<T>): value is None {
  return (value === null || value === undefined)
}
