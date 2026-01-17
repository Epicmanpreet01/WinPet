import os

VALID_EXTENSIONS = {'.png', '.jpg', '.jpeg'}


def has_valid_frames(path):
  if not os.path.isdir(path):
    return False

  for name in os.listdir(path):
    base, ext = os.path.splitext(name)
    if base.isdigit() and ext.lower() in VALID_EXTENSIONS:
      return True
  return False


def is_valid_sequence(base_path):
  idle_path = os.path.join(base_path, 'idle')
  picked_path = os.path.join(base_path, 'picked')

  return (
    os.path.isdir(base_path)
    and has_valid_frames(idle_path)
    and has_valid_frames(picked_path)
  )
