'use client'

import { useState } from 'react'
import { Moon, Sun, FileText, Github, Apple } from 'lucide-react'
import { Button } from "@/app/ui/button"
import { Input } from "@/app/ui/input"
import { Label } from "@/app/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/app/ui/card"
import Image from 'next/image'


export default function SignUpPage() {

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background text-foreground">
      
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex justify-center mb-4">
          <Image src= "/logo-sm.png" width= {512} height = {512} alt = "logo" className="h-12 w-12" />

          </div>
          <CardTitle className="text-center">Create an account</CardTitle>
          <CardDescription className="text-center">
            Sign up for DocShare to start sharing your documents
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" type="text" placeholder="John Doe" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="john@example.com" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirm-password">Confirm Password</Label>
              <Input id="confirm-password" type="password" required />
            </div>
            <Button type="submit" className="w-full">Sign Up</Button>
          </form>
          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-muted-foreground"></span>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <Button variant="outline">
              <Github className="h-5 w-5" />
              <span className="sr-only">GitHub</span>
            </Button>
            <Button variant="outline">
              <Apple className="h-5 w-5" />
              <span className="sr-only">Apple</span>
            </Button>
            <Button variant="outline">
              <svg className="h-5 w-5" viewBox="0 0 24 24">
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
                <path d="M1 1h22v22H1z" fill="none" />
              </svg>
              <span className="sr-only">Google</span>
            </Button>
          </div>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-muted-foreground">
            Already have an account?{' '}
            <a href="/login" className="text-primary hover:underline">
              Sign in
            </a>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}