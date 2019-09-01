#!/usr/bin/env python3

from aws_cdk import core

from cdk.web_application_stack import CdkStack


app = core.App()
CdkStack(app, "MythicalMysfits-Website")

app.synth()
