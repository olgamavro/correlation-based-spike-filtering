from collections import defaultdict


def pos_to_id(row: int, col: int, grid_side: int = 16) -> int:
    """Convert a row and column position to a neuron ID."""
    return row * grid_side + col


def id_to_pos(neuron_id: int, grid_side: int = 16) -> tuple[int, int]:
    """Convert a neuron ID to a row and column position."""
    return divmod(neuron_id, grid_side)


def tile_center(tile_index: int, tile_side: int = 4, blob_side: int = 4) -> tuple[int, int]:
    """
    Return the center position of a tile.

    By default, this assumes a 16x16 neuron grid split into 4x4 tiles.
    """
    tile_row = tile_index // tile_side
    tile_col = tile_index % tile_side

    center_row = tile_row * blob_side + blob_side // 2
    center_col = tile_col * blob_side + blob_side // 2

    return center_row, center_col


def square_blob_ids(
    center_row: int,
    center_col: int,
    side: int,
    grid_side: int = 16,
) -> list[int]:
    """Return neuron IDs inside a square region."""
    half = side // 2
    ids = []

    for row in range(center_row - half, center_row + half):
        for col in range(center_col - half, center_col + half):
            if 0 <= row < grid_side and 0 <= col < grid_side:
                ids.append(pos_to_id(row, col, grid_side))

    return ids


def make_square_populations(
    n_populations: int,
    blob_side: int = 4,
    grid_side: int = 16,
) -> dict[int, list[int]]:
    """
    Create square neuron populations on a 2D grid.

    Returns a dictionary like:
        {
            0: [neuron ids...],
            1: [neuron ids...],
            ...
        }
    """
    populations = defaultdict(list)

    for population_id in range(n_populations):
        center_row, center_col = tile_center(
            population_id,
            tile_side=grid_side // blob_side,
            blob_side=blob_side,
        )

        populations[population_id] = square_blob_ids(
            center_row=center_row,
            center_col=center_col,
            side=blob_side,
            grid_side=grid_side,
        )

    return dict(populations)