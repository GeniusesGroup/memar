/* For license and copyright information please see the LEGAL file in the code repository */

package email

// [comment, `email`, object] >>

// Policy (rule):::
// - Object MUST has related mediatype like SMTP format.
// - all email data such as subject, from, to, cc, bc, ... store in an object and relate to the comment
//       https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol#SMTP_transport_example
// and will be relate in real system data not text version of it e.g. `comment` relate to `user` not `username text`
// -
