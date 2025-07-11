# Clear all restarted containers (excluding Succeeded pods)
for namespace in $(kubectl get namespace -o=json | jq -r '.items[].metadata.name'); do
  echo "Processing namespace ${namespace}"
  kubectl -n "${namespace}" get pods -o=json \
  | jq -r '.items[]
      | select(.status.phase != "Succeeded")
      | select(.status.containerStatuses[]?.restartCount >= 1)
      | .metadata.name' \
  | xargs --no-run-if-empty kubectl -n "${namespace}" delete pod
done
