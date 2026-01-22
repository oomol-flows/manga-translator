# Troubleshooting Guide

## ImportError: libGL.so.1 missing

### Error
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

### Cause
Missing system library required by OpenCV (cv2).

### Solution
The bootstrap script in [package.oo.yaml](package.oo.yaml#L8) already includes the fix:
```bash
apt-get update && apt-get install libgl1 -y
apt-get install libglib2.0-0 -y
```

This runs automatically when the OOMOL container is initialized.

**Manual fix** (for development environment):
```bash
apt-get update && apt-get install -y libgl1 libglib2.0-0
```

---

## ModuleNotFoundError: No module named 'paddle'

### Error
```
ModuleNotFoundError: No module named 'paddle'
```

### Cause
PaddlePaddle is not installed. This is a heavy ML framework required by manga_translator_core.

### Solution
The bootstrap script in [package.oo.yaml](package.oo.yaml#L14-L20) handles PaddlePaddle installation:
```bash
if command -v nvidia-smi &> /dev/null; then
  pip install paddlepaddle-gpu==2.6.2
else
  pip install paddlepaddle==2.6.2
```

This runs automatically in the OOMOL container environment.

**Manual fix** (for development environment):
```bash
# For CPU
pip install paddlepaddle==2.6.2

# For GPU (if CUDA available)
pip install paddlepaddle-gpu==2.6.2
```

---

## Import Errors in Development Environment

### Context
When testing imports directly with `python3 -c "from shared.manga_translator..."` in the development environment, you may encounter:

1. `libGL.so.1` missing
2. `paddle` module missing
3. Other ML library issues

### Why This Happens
The `manga_translator_core` package has heavy dependencies that are:
- Installed automatically in OOMOL containers via bootstrap
- May not be present in development/testing environments

### Expected Behavior

**✓ In OOMOL Container** (after bootstrap runs):
- All dependencies installed
- All imports work
- Flows execute successfully

**✗ In Development Environment** (without bootstrap):
- Import errors expected
- This is normal and doesn't indicate a problem with the migration

### Verification
To verify the migration was successful:

1. **Check code structure**:
   ```bash
   ls -la shared/manga_translator_core/
   ```
   Should show all modules extracted from the submodule.

2. **Check import paths are updated**:
   ```bash
   grep -r "from manga_translator" shared/manga_translator/
   ```
   Should show imports from `shared.manga_translator_core`, not `manga_translator`.

3. **Run a flow in OOMOL**:
   ```bash
   # This is the definitive test
   runFlow /app/workspace/flows/translate-manga-book/flow.oo.yaml
   ```
   If it completes, the migration is successful.

---

## Migration Validation Checklist

- [x] `manga_translator_core/` directory exists in `shared/`
- [x] `shared/manga_translator/` imports updated to use `shared.manga_translator_core`
- [x] `.gitmodules` file removed
- [x] `manga/` submodule removed from git
- [x] `package.oo.yaml` bootstrap script updated (submodule lines removed)
- [x] System dependencies (libgl1, libglib2.0-0) in bootstrap
- [x] PaddlePaddle installation in bootstrap
- [x] Flow test completed successfully

All checkpoints passed ✓
