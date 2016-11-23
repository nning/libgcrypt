/* ecc-gots.c  -  Elliptic Curve GOST signatures
 * Copyright (C) 2007, 2008, 2010, 2011 Free Software Foundation, Inc.
 * Copyright (C) 2013 Dmitry Eremin-Solenikov
 *
 * This file is part of Libgcrypt.
 *
 * Libgcrypt is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of
 * the License, or (at your option) any later version.
 *
 * Libgcrypt is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; if not, see <http://www.gnu.org/licenses/>.
 */

#include <config.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "g10lib.h"
#include "mpi.h"
#include "cipher.h"
#include "context.h"
#include "ec-context.h"
#include "ecc-common.h"
#include "pubkey-internal.h"


/* Compute an GOST R 34.10-01/-12 signature.
 * Return the signature struct (r,s) from the message hash.  The caller
 * must have allocated R and S.
 */
gpg_err_code_t
_gcry_ecc_gost_sign (gcry_mpi_t input, ECC_secret_key *skey,
                     gcry_mpi_t r, gcry_mpi_t s)
{
  return GPG_ERR_UNSUPPORTED_ALGORITHM;
}


/* Verify a GOST R 34.10-01/-12 signature.
 * Check if R and S verifies INPUT.
 */
gpg_err_code_t
_gcry_ecc_gost_verify (gcry_mpi_t input, ECC_public_key *pkey,
                       gcry_mpi_t r, gcry_mpi_t s)
{
  return GPG_ERR_UNSUPPORTED_ALGORITHM;
}
