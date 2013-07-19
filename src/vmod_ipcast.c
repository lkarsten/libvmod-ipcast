#include <stdlib.h>

#include "vrt.h"
#include "bin/varnishd/cache.h"

#include "vcc_if.h"

#include <sys/socket.h>
#include <netdb.h>

int
init_function(struct vmod_priv *priv, const struct VCL_conf *conf) {
	return (0);
}

void vmod_clientip(struct sess *sp, const char *ipstring) {
	struct addrinfo hints;
	struct addrinfo *rp;
	int s;

	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_UNSPEC;

	// Don't attempt DNS resolution.
	hints.ai_flags = AI_NUMERICHOST;
	hints.ai_protocol = 0;

	s = getaddrinfo(ipstring, NULL, &hints, &rp);
	if (s != 0) {
		VSL(SLT_Debug, 0, "ipcast: Unable to decode IP address '%s'", ipstring);
		VSL(SLT_Debug, 0, "ipcast: getaddrinfo(): %s", gai_strerror(s));
		return;
	}

	sp->sockaddrlen = rp->ai_addrlen;
	memcpy(sp->sockaddr, rp->ai_addr, sizeof(struct sockaddr_storage));

	freeaddrinfo(rp);
}
