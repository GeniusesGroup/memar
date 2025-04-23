/* For license and copyright information please see the LEGAL file in the code repository */

package approved

// [quiddity, `approved_by`, user] >>
// [quiddity, `approved_by`, group] >>
//
// [user, `approved`, quiddity] >>
// [group, `approved`, quiddity] >>

// Policy (rule):::
// quiddity CAN be e.g. `request`, `law`, `task`, `contract`, ...
//
// SignatureBy or ApprovedBy means user accept the contract agreements
// Signature will store by related request in `audit-request`.
// SignatureBy
