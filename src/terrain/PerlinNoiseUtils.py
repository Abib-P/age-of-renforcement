from perlin_noise import PerlinNoise


def generate_map(width: int, height: int, octaves: [int], lacunarity: float):
    noise_list: [PerlinNoise] = []
    for octave in octaves:
        noise_list.append(PerlinNoise(octaves=octave))

    map = []
    for i in range(height):
        row: [float] = []
        for j in range(width):
            noise_val: float = 0
            noise_scale: float = 1
            for noise in noise_list:
                noise_val += noise_scale * noise([i / width, j / height])
                noise_scale *= lacunarity
            row.append(noise_val)
        map.append(row)

    return map
