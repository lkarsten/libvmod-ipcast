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



static struct sockaddr_storage *
parse_ip(struct sess *sp, const char *ipstring) {
	struct addrinfo hints;
	struct addrinfo *rp;
	int s;
	void *res;

	AN(sp);
	AN(ipstring);

	res = WS_Alloc(sp->ws, sizeof (struct sockaddr_storage));
	AN(res);

	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_UNSPEC;

	// Don't attempt DNS resolution.
	hints.ai_flags = AI_NUMERICHOST;

	s = getaddrinfo(ipstring, NULL, &hints, &rp);
	if (s != 0) {
		VSL(SLT_VCL_Log, 0, "ipcast: Unable to decode IP address '%s'",
				ipstring);
		VSL(SLT_VCL_Log, 0, "ipcast: getaddrinfo(): %s", gai_strerror(s));
		return(NULL);
	}
	AN(rp);

	assert(rp->ai_addrlen == 16 || rp->ai_addrlen == 28);
	memcpy(res, rp->ai_addr, rp->ai_addrlen);
	freeaddrinfo(rp);
	return (res);
}


static pthread_mutex_t priv_mtx = PTHREAD_MUTEX_INITIALIZER;

struct sockaddr_storage *
vmod_ip(struct sess *sp, struct vmod_priv *priv, const char *ipstring,
    const char *d)
{
	void *res;
	CHECK_OBJ_NOTNULL(sp, SESS_MAGIC);
	if (priv->priv == NULL) {
		AZ(pthread_mutex_lock(&priv_mtx));
		if (priv->priv == NULL) {
			struct sockaddr_storage *p = parse_ip(sp, d);
			/* XXX: if we can't parse the fallback, we crash. */
			AN(p);
			priv->priv = malloc(sizeof *p);
			AN(priv->priv);
			memcpy(priv->priv, p, sizeof *p);
			priv->free = free;
		}
		AZ(pthread_mutex_unlock(&priv_mtx));
	}

	if (!ipstring) {
		VSL(SLT_VCL_Log, 0, "ipcast: NULL is not an IP address");
		return (priv->priv);
	}

	res = parse_ip(sp, ipstring);
	if (res)
		return (res);
	return (priv->priv);
}
