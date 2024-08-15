# Security Policy

## Overview

This repository is committed to maintaining the security of our users and their data. We take potential vulnerabilities very seriously and appreciate your assistance in responsibly disclosing any security issues.

## Reporting a Vulnerability

If you discover a security vulnerability within our application, please report it to us immediately. To report a vulnerability, please send an email to gssoc@girlscript.tech
 with details about the issue. Please include the following information:
- A detailed description of the vulnerability.
- Steps to reproduce the vulnerability.
- The impact of the vulnerability.
- Any potential fixes or suggestions.

We will review your report, acknowledge it within 48 hours, and work on a fix as quickly as possible.

## Bug Summary

### Issue: Unauthorized Access to Certificate Verification and Download

#### Description:
A critical security vulnerability was identified in the certificate verification feature of the Girl Script Summer of Code website. The issue allows any user to verify and download certificates using someone else's email address. The lack of authentication and verification of the user's identity before granting access to the certificate is the root cause of this vulnerability.

#### Impact:
- **Privacy Violation**: Unauthorized users can download certificates containing personal information.
- **Data Misuse**: Sensitive data such as names and achievements can be accessed by malicious actors, leading to potential misuse.

#### Mitigation:
- Implement strict authentication mechanisms that verify the user's identity before allowing access to certificate downloads.
- Consider implementing a token-based system where a unique, time-limited token is sent to the registered email address, which must be used to access the certificate.
- Regularly review and update security practices to protect user data.

## Scope

This security policy applies to all aspects of the project, including the main application, its dependencies, and any third-party services that are integrated.

## Responsible Disclosure

We ask that any security vulnerabilities are reported to us directly and not disclosed publicly until a fix has been implemented. This allows us to address the issue promptly without exposing users to unnecessary risk.

Thank you for helping to keep our community safe.

