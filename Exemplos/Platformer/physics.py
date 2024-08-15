def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement.x
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement.x > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement.x < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement.y
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement.y > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement.y < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types