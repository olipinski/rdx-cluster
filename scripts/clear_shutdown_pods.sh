# Clear all nodeShutdown containers
for namespace in $(kubectl get namespace -o=json |  jq -r '.items[] .metadata.name') ; do
  echo "Processing namespace ${namespace}"
  kubectl -n ${namespace} get pod -o=json \
  | jq '[.items[] | select(.status.reason=="Evicted")]' \
  | jq -r '.[] .metadata.name' \
  | xargs --no-run-if-empty kubectl -n ${namespace} delete pod
done
