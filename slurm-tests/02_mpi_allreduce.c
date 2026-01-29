#include <mpi.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);

  int rank, size;
  char host[256];
  gethostname(host, sizeof(host));

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  long x = rank + 1;
  long sum = 0;

  MPI_Allreduce(&x, &sum, 1, MPI_LONG, MPI_SUM, MPI_COMM_WORLD);

  if (rank == 0) {
    long expected = (long)size * (size + 1) / 2;
    printf("MPI size=%d  allreduce_sum=%ld  expected=%ld  %s\n",
           size, sum, expected, (sum == expected) ? "OK" : "FAIL");
  }

  printf("rank=%d/%d host=%s\n", rank, size, host);

  MPI_Finalize();
  return 0;
}
