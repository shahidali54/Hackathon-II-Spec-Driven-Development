// "use client";

// import { useState } from "react";
// import { useForm } from "react-hook-form";
// import Link from "next/link";
// import { useRouter } from "next/navigation";
// import { useAuth } from "@/hooks/useAuth";
// import { Button } from "@/components/ui/Button";
// import { Input } from "@/components/ui/Input";
// import { isValidEmail, isValidPassword } from "@/lib/utils";

// interface SignUpFormData {
//   email: string;
//   password: string;
//   confirmPassword: string;
// }

// export function SignUpForm() {
//   const router = useRouter();
//   const { signUp, signIn, isLoading, error, clearError } = useAuth();
//   const [submitError, setSubmitError] = useState<string | null>(null);

//   const {
//     register,
//     handleSubmit,
//     watch,
//     formState: { errors },
//   } = useForm<SignUpFormData>({
//     defaultValues: { email: "", password: "", confirmPassword: "" },
//   });

//   const password = watch("password");

//   const onSubmit = async (data: SignUpFormData) => {
//     setSubmitError(null);
//     clearError();
//     try {
//       await signUp(data.email, data.password);
//       await signIn(data.email, data.password);
//       router.push("/dashboard");
//     } catch (err) {
//       const message = err instanceof Error ? err.message : "Sign up failed";
//       setSubmitError(message);
//     }
//   };

//   const displayError = submitError || error;

//   return (
//     <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
//       {displayError && (
//         <div className="p-3 text-sm text-red-600 bg-red-50 dark:bg-red-900/20 dark:text-red-400 rounded-lg">
//           {displayError}
//         </div>
//       )}

//       <Input
//         label="Email"
//         type="email"
//         placeholder="you@example.com"
//         error={errors.email?.message}
//         {...register("email", {
//           required: "Email is required",
//           validate: (value) => isValidEmail(value) || "Please enter a valid email",
//         })}
//       />

//       <Input
//         label="Password"
//         type="password"
//         placeholder="Create a password"
//         helperText="Must be at least 8 characters"
//         error={errors.password?.message}
//         {...register("password", {
//           required: "Password is required",
//           validate: (value) =>
//             isValidPassword(value) || "Password must be at least 8 characters",
//         })}
//       />

//       <Input
//         label="Confirm Password"
//         type="password"
//         placeholder="Confirm your password"
//         error={errors.confirmPassword?.message}
//         {...register("confirmPassword", {
//           required: "Please confirm your password",
//           validate: (value) => value === password || "Passwords do not match",
//         })}
//       />

//       <Button type="submit" fullWidth isLoading={isLoading}>
//         Create Account
//       </Button>

//       <p className="text-center text-sm text-zinc-600 dark:text-zinc-400">
//         Already have an account?{" "}
//         <Link
//           href="/auth/signin"
//           className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400"
//         >
//           Sign in
//         </Link>
//       </p>
//     </form>
//   );
// }


"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { isValidEmail, isValidPassword } from "@/lib/utils";

interface SignUpFormData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  confirmPassword: string;
}

export function SignUpForm() {
  const router = useRouter();
  const { signUp, signIn, isLoading, error, clearError } = useAuth();
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SignUpFormData>();

  const password = watch("password");

  const onSubmit = async (data: SignUpFormData) => {
    setSubmitError(null);
    clearError();

    try {
      await signUp({
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
        password: data.password,
        is_active: true,
      });

      await signIn(data.email, data.password);
      router.push("/dashboard");
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "Signup failed");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {(submitError || error) && (
        <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg">
          {submitError || error}
        </div>
      )}

      <Input
        label="First Name"
        error={errors.first_name?.message}
        {...register("first_name", { required: "First name is required" })}
      />

      <Input
        label="Last Name"
        error={errors.last_name?.message}
        {...register("last_name", { required: "Last name is required" })}
      />

      <Input
        label="Email"
        type="email"
        error={errors.email?.message}
        {...register("email", {
          required: "Email is required",
          validate: (v) => isValidEmail(v) || "Invalid email",
        })}
      />

      <Input
        label="Password"
        type="password"
        error={errors.password?.message}
        helperText="Minimum 8 characters"
        {...register("password", {
          required: "Password is required",
          validate: (v) =>
            isValidPassword(v) || "Minimum 8 characters",
        })}
      />

      <Input
        label="Confirm Password"
        type="password"
        error={errors.confirmPassword?.message}
        {...register("confirmPassword", {
          validate: (v) => v === password || "Passwords do not match",
        })}
      />

      <Button type="submit" fullWidth isLoading={isLoading}>
        Create Account
      </Button>

      <p className="text-center text-sm text-zinc-600">
        Already have an account?{" "}
        <Link href="/auth/signin" className="text-blue-600 font-medium">
          Sign in
        </Link>
      </p>
    </form>
  );
}
      </p>
    </form>
  );
}
