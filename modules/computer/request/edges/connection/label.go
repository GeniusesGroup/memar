/* For license and copyright information please see the LEGAL file in the code repository */

package connection

// [request, `called_by`, connection] >>
//
// [connection, `called`, request] >>

// Policy (rule):::
// Store to help us answer these questions:
// - AppInstance request came from
// - UserID of hardware owner
// - Is it official GUI app or SDK or API call
