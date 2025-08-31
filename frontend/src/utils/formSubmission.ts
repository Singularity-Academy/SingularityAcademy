import { saveAs } from 'file-saver';

export interface FormSubmission {
  type: 'mentor' | 'partner' | 'donation' | 'signup';
  timestamp: string;
  data: Record<string, any>;
}

export const saveFormSubmission = async (formData: FormSubmission): Promise<void> => {
  try {
    // Create a formatted filename with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${formData.type}-submission-${timestamp}.json`;
    
    // Create the JSON content
    const jsonContent = JSON.stringify(formData, null, 2);
    
    // Create a blob and save it
    const blob = new Blob([jsonContent], { type: 'application/json' });
    saveAs(blob, filename);
    
    console.log(`Form submission saved: ${filename}`);
  } catch (error) {
    console.error('Error saving form submission:', error);
    throw new Error('Failed to save form submission');
  }
};

export const createFormSubmission = (
  type: FormSubmission['type'],
  data: Record<string, any>
): FormSubmission => {
  return {
    type,
    timestamp: new Date().toISOString(),
    data
  };
};