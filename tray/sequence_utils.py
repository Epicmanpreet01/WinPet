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
  if not os.path.isdir(base_path):
    return False

  idle_path = os.path.join(base_path, 'idle')

  if not has_valid_frames(idle_path):
    return False

  for name in os.listdir(base_path):
    state_path = os.path.join(base_path, name)

    if not os.path.isdir(state_path):
      continue

    if name == 'idle':
      continue

    if not has_valid_frames(state_path):
      return False

  return True
