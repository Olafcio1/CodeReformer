def RGB(value: tuple[float, float, float]) -> tuple[int, int, int]:
	return [int(out * 255) for out in value]
