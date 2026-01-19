
## 2026-01-19 — SSH password toggle playbook
- Added `playbooks/ssh-password-toggle.yml` to flip `PasswordAuthentication yes/no` directly in `/etc/ssh/sshd_config`, validate with `sshd -t`, and restart sshd only on valid changes.
- Exact line managed: `PasswordAuthentication {{ ssh_password_auth }}`.

Run commands:
- Unlock (enable password auth):
  ansible-playbook -i inventories/inventory.ini playbooks/ssh-password-toggle.yml -e ssh_password_auth=yes
- Lock (disable password auth):
  ansible-playbook -i inventories/inventory.ini playbooks/ssh-password-toggle.yml -e ssh_password_auth=no
