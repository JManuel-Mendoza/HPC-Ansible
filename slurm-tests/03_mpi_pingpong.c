#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static double now() { return MPI_Wtime(); }

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size < 2) {
        if (rank == 0) fprintf(stderr, "Need at least 2 ranks\n");
        MPI_Finalize();
        return 1;
    }

    int partner = (rank == 0) ? 1 : 0;
    int msg_bytes = (argc > 1) ? atoi(argv[1]) : (1 << 20);   // default 1 MiB
    int iters     = (argc > 2) ? atoi(argv[2]) : 200;
    int warmup    = 50;

    char *buf = (char*)malloc(msg_bytes);
    memset(buf, 0xAB, msg_bytes);

    MPI_Barrier(MPI_COMM_WORLD);

    // warmup
    for (int i = 0; i < warmup; i++) {
        if (rank == 0) {
            MPI_Send(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD);
            MPI_Recv(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        } else if (rank == 1) {
            MPI_Recv(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD);
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);

    double t0 = 0.0, t1 = 0.0;
    if (rank == 0) t0 = now();

    for (int i = 0; i < iters; i++) {
        if (rank == 0) {
            MPI_Send(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD);
            MPI_Recv(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        } else if (rank == 1) {
            MPI_Recv(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(buf, msg_bytes, MPI_BYTE, partner, 0, MPI_COMM_WORLD);
        }
    }

    if (rank == 0) {
        t1 = now();
        double total_s = (t1 - t0);
        double rt_s = total_s / iters;                 // round-trip seconds
        double one_way_s = rt_s / 2.0;
        double bw_GBps = (double)msg_bytes / one_way_s / 1e9;

        printf("PingPong ranks 0<->1 msg=%d bytes iters=%d\n", msg_bytes, iters);
        printf("RTT=%.3f ms  one-way=%.3f ms  approx_bw=%.3f GB/s\n",
               rt_s*1e3, one_way_s*1e3, bw_GBps);
    }

    free(buf);
    MPI_Finalize();
    return 0;
}
